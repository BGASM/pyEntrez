"""Main entry-point into pyEntrez, handling cmdline args and initializing prompt or TUI service.

When script is started the user will be checked against local user file; if they are a first-time
user they willwill go through a new user creation via the user_cred module and then return. If they
are a returning user their settings file will be loaded and a configargparser will be created. The
cmdline arguments are contained within the pyentrez.utils.variables module, where new arguments can
be added or removed. All settings in variables module are added to the users environment. Finally,
after parsing args either the prompt or TUI environment will initialize.

py-cui is extended in this module for the purpose of hooking into their resize-refresh activity
with a threaded monitor. This hook calls for all text containing widgets to update their text-
wrappers and to refresh.
"""
import threading
import time
# configparser Library
from pathlib import Path
from typing import Any, Optional, Tuple

import attr
import configargparse
# Py_CUI Library
import py_cui
from configargparse import ArgumentParser, argparse
# Logger
from loguru import logger

import pyentrez
from pyentrez import exceptions
from pyentrez.main import cmd_entrez, entrez_manager
from pyentrez.main import user_cred as uc
from pyentrez.utils import envars as ev
from pyentrez.utils import logger_utils as lu
from pyentrez.utils import string_utils as su
from pyentrez.utils import variables as vl

cuxy: Tuple[int, int] = (5, 4)


# noinspection PyPep8Naming
class MyCUI(py_cui.PyCUI):
    """Extension of PyCUI for hooking into _refresh_height_width

    PyCui has a built in resize handler from curses, which calls for all widgets to refresh their
    terminal character height and width. There was no built-in functionality for resizing string
    contained within those widgets. This class extension provides a hook by passing in the instanced
    EntrezManager and calling for text_wrapping whenever _refresh_height_width is called.

    Since py_cui checks and calls refreshes several times per second if the user is still resizing
    their terminal, a thread is started to monitor for refresh calls, instead of calling each time.
    The threaded call sets a progress bool to true that prevents new threads from being started
    until this one is complete. The thread takes a short sleep, and then calls for EntrezManager
    to call its refresh method with the latest height and width values.

    Args:
        num_rows (int): number of row
        num_cols (int): number of cloumns
        **kwargs (Dict[str, Any]: All other arguments required by parent.

    Attributes:
            lowermanager: Instance of EntrezManager
            timing: bool to prevent multiple refresh monitor threads
    """

    def __init__(self, num_rows, num_cols, **kwargs):
        super().__init__(num_rows, num_cols, **kwargs)
        self.lowermanager: Optional[Any] = None
        self.thread: Optional[Any] = None
        self.timing = False

    # Start of pyEntrez-extended code ----------------------------
    def start_time(self):
        """Only start a new thread once per time interval by setting a timing checkpoint."""
        if not self.timing:
            self.timing = True
            self.thread = threading.Thread(target=self.timer, args=())
            self.thread.start()

    def timer(self):
        """On a new thread, when called sleep, and then call for EntrezManager to refresh."""
        assert self.lowermanager is not None
        time.sleep(0.05)
        self.lowermanager.refresh_h_w()
        self.timing = False

    def _refresh_height_width(self, height, width):
        """Function that updates the height and width of the CUI based on terminal window size

        Args:
            height (int): Window height in terminal characters
            width (int):Window width in terminal characters
        """

        if self.lowermanager is not None:
            self.start_time()

        # End of pyEntrez-extended code ----------------------------
        self._height = height
        self._width = width
        self._grid.update_grid_height_width(self._height, self._width)
        for widget_id in self._widgets.keys():
            self._widgets[widget_id].update_height_width()
        if self._popup is not None:
            self._popup.update_height_width()


@attr.s(slots=True)
class GetParser(object):
    path = attr.ib()
    args = attr.ib()

    @classmethod
    def get_parser(cls) -> Any:  # noqa: WPS213
        """Check if new user and then create argparser.

        Function will run check_new() function to check if this is user's
        first time using the script, and if it is a settings directory will
        be created and a copy of the default config copied to it.

        Additionally, the new user will be added to the core_config.yaml file,
        with a path to the user's my_settings.yaml file.

        ConfigArgParser allows for setting default config paths and will
        check defaults>user_settings>envar.
        User can also pass --INIT arg to create a new workspace.

        Settings in pyentrez.utils.variables are formatted as follows:
        APPSETTING = [
            {
                'args': ['-c', '--credentials'],
                'kwargs': {
                    'action': 'store_true',
                    'default': False,
                    'help': 'Allow user to set DB credentials on application start.',
                },
                'setting': {'envar': <envar>, 'text': <text>}
            },
            ...

        Returns:
            A tuple containing:
            An instance of configargparser generated with arguments define in
            pyentrez.utils.varaibles.
            The os-agnostic Path to user's workspace directory.
        """
        path = uc.check_new()
        parse = configargparse.ArgParser(
            default_config_files=[
                path / 'my_settings.yaml',
            ],
            formatter_class=argparse.MetavarTypeHelpFormatter,
            add_env_var_help=False,
            add_config_file_help=False,
            auto_env_var_prefix=None,
            description='''
                        pyEntrez can be run as a TUI or from the command line. Args that start
                        with "--" (eg. --version) can also be set in a config file. The config file
                        uses YAML syntax and must represent a YAML "mapping" (for details, see
                        http://learn.getgrav.org/advanced/yaml). If an arg is specified in more
                        than one place, then commandline values override config file values
                        which override defaults.
                        ''')
        menu = vl.get_settings()
        for organization in menu.values():
            for setting in organization:
                if 'args' and 'kwargs' in setting.keys():
                    parse.add(*setting['args'], **setting['kwargs'])
        args = parse.parse_args()
        args = vars(args)
        return cls(path, args)


@attr.s
class CLI(object):
    version: str = attr.ib(default=pyentrez.__version__)
    copyright: str = attr.ib(default=pyentrez.__copyright__)
    catastrophic_failure: Optional[bool] = attr.ib(default=None)
    args: Any = attr.ib(init=False)

    def initialize(self):
        parser = GetParser.get_parser()
        self.args = parser.args
        self.args['Home'] = parser.path

    def run_pyentrez(self):
        if self.args['version']:
            print(f'pyentrez - {self.version}')
            print(self.copyright)
            raise SystemExit(self.catastrophic_failure)
        elif self.args['INIT']:
            uc.first_run()
        else:
            pyentrez.configure_logger(self.args['verbose'], self.args['output'])
            ev.setenv(self.args)
            if self.args['TUI'] == 'on':
                self.starttui()
            else:
                self.notui()

    def notui(self) -> None:
        """Initialize application in commandline prompt mode."""
        tui = cmd_entrez.CommandEntrez()
        tui.start()

    def starttui(self) -> None:
        """Initiate script in TUI mode.

        Initialize pyCUI root and the EntrezManager. All config settings have been saved to envars
        earlier in script. We use our extended myCUI class to hook into py_cui's resize refresh.
        """
        root = MyCUI(cuxy[0], cuxy[1])
        root.toggle_unicode_borders()
        em = entrez_manager.EntrezManager(root)  # noqa: F841
        root.entrez_manager = em
        root.start()

    def clean_exit(self) -> None:
        """Provides a clean exit with logging and file closing."""
        logger.info('Exiting pyEntrez.')
        logger.info('-----------------------------------------------------')
        raise SystemExit(self.catastrophic_failure)

    def _run(self):
        self.initialize()
        self.run_pyentrez()

    @logger.catch
    def execute(self) -> None:
        """Entry point into our script that instances a parser and then selects start behavior.

        Instance a configargparser and check if user is new or existing. Parse the returned args
        and determine if full initialization is taking place or if we are creating a new user or
        returning version info. If initialization of application is requested, call for all setting
        arguments to be loaded to envars and either start application in cmd-prompt or TUI mode.

        Args that effect start behavior:
            --INIT: Allows existing user to create a new workspace directory.
            --version: Prints pyentrez version info and exits the application.
            --TUI <on|off): Run application in TUI mode if 'on', or in cmd-prompt mode if 'off'
        """
        try:
            self._run()
        except KeyboardInterrupt as exc:
            print('... stopped')
            logger.critical(f'Caught keyboard interrupt from user:{exc}')
            self.catastrophic_failure = True
        except exceptions.ExecutionError as exc:
            logger.critical(f'There was a critical error during execution of pyEntrez: {exc}')
            print(f'There was a critical error during execution of pyEntrez: {exc}')
            self.catastrophic_failure = True
        except exceptions.EarlyQuit:
            logger.critical('... stopped while processing files')
            print("... stopped while processing files")
            self.catastrophic_failure = True
