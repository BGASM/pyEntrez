from typing import Any, Dict, List, Optional, Tuple, Union

import attr
import py_cui
import py_cui.widgets
from loguru import logger

import pyentrez
from pyentrez import exceptions
from pyentrez.utils import envars as ev
from pyentrez.utils import logic
from pyentrez.utils import string_utils as su

string_comm = Tuple[Union[str, int], Any]
dict_comm = Dict[Any, List[string_comm]]


@attr.s
class ScreenManager(object):
    """Main parent screen manager class.

    Contains common functionality for showing command results,
    handling credentials, commands, and long operations.

    Attributes:
        manager (pyEntrezManager):   Driver engine manager
        message (str):      variable to store messages accross functions
        status (int):       variable to store status codes accross function
        utility_var (obj):  variable to store any data accross functions
    """

    manager: Any = attr.ib(kw_only=True)
    scraper: Any = attr.ib(kw_only=True)
    setting_message: Optional[str] = attr.ib(init=False, default='Master Screen Manager')
    screen_type: str = attr.ib(init=False, default='manager')
    info_panel: Any = attr.ib(init=False)
    menu_choices: List[Any] = attr.ib(init=False,
                                      default=[
                                          'Enter Credentials',
                                          'DB List',
                                          'About',
                                          'Exit',
    ])

    def show_menu_popup(self):
        menu_choices = ['Fetch', 'Review', 'Settings', 'Exit']
        self.manager.root.show_menu_popup('Make a selection.', menu_choices,
                                          self.process_menu_selection)

    def process_menu_selection(self, selection) -> None:
        """Execute based on user menu selection.

        Override of base class.

        Args:
            selection (str): string that was highlighted when the enter key hit.
        """
        if selection == 'Fetch':
            self.manager.open_window('FETCH')
        elif selection == 'Review':
            self.manager.open_window('REVIEW')
        elif selection == 'Settings':
            self.manager.open_window('SET')
        elif selection == 'Exit':
            raise exceptions.CleanExit()


@attr.s(kw_only=True)
class ScreenProcessor(ScreenManager):
    """Placeholder."""

    message = attr.ib(init=False)
    status = attr.ib(init=False, default=0)
    def initialize_screen_elements(self) -> None:
        """Function that must be overridden by subscreen.

        Creates py_cui_widgets, returns widget set object.
        """

    def show_menu(self) -> None:
        """Opens the menu using the menu item list."""

    def refresh_status(self) -> None:
        """Function that is fired after each git operation.

        Implement in subclasses.
        """

    def update_info(self, msg: str) -> None:
        """Wipes and replaces text on the main info panel.

        Args:
            msg (str): String of what needs to be printed on info block.

        ..
        """

    def set_initial_values(self) -> None:
        """Function that initializes status bar for Fetch screen."""

    def clear_elements(self, *args):
        """Placeholder."""

    def load_db(self):
        logger.debug("Loading new DB.")
        self.message, self.status = self.manager.load_db()
        self.refresh_settings()
        self.manager.root.stop_loading_popup()

    def refresh_settings(self):
        """Placeholder."""

    def show_command_result(self,
                            out,
                            err: int,
                            show_on_success=True,
                            command_name='Command',
                            success_message='Success',
                            error_message='Error'
                            ):
        """Function that displays the result of stdout/err for an external command.

        Parameters
        ----------
        out : str
            stdout string from command
        err : str
            stderr string from command
        show_on_success : bool
            Set to false to show no messages on success. (ex. git log doesnt need success message)
        command_name : str
            name of command run.
        success_message : str
            message to show on successful completion
        error_message : str
            message to show on unsuccessful completion
        """

        show_in_box = False
        stripped_output = out.strip()
        if len(out.splitlines()) > 1:
            popup_message = "Check Info Box For {} Output".format(command_name)
            show_in_box = True
        else:
            popup_message = stripped_output
        if err != 0:
            self.manager.root.show_error_popup(error_message, popup_message)
        elif show_on_success:
            self.manager.root.show_message_popup(success_message, popup_message)
        if show_in_box and (err != 0 or show_on_success):
            box_out = out
            if err != 0:
                err_out = '\n'
                temp = out.splitlines()
                for line in temp:
                    err_out = err_out + '- ' + line + '\n'
                box_out = err_out
            self.info_panel.title = '{} Output'.format(command_name)
            self.info_panel.set_text(box_out)

    def show_status_long_op(self, name='Command', succ_message="Success", err_message = "Error"):
        """Shows the status of a long(async) operation on success completion

        Parameters
        ----------
        name : str
            name of command run.
        succ_message : str
            message to show on successful completion
        err_message : str
            message to show on unsuccessful completion
        """

        logger.debug("In show_status.")
        self.show_command_result(self.message,
                                 self.status,
                                 command_name=name,
                                 success_message=succ_message,
                                 error_message=err_message,
        )
        self.message = ''
        self.status = 0

    def execute_long_operation(self, loading_message, long_op_function):
        """Wrapper function that allows for executing long operations w/ credential requirements.

        Parameters
        ----------
        loading_message : str
            Message displayed while async op is performed
        long_op_function : no-arg or lambda function
            Function that is fired in an async second thread
        """

        self.manager.perform_long_operation(loading_message, long_op_function,
                                            self.show_status_long_op)

@attr.s
class WidgetRing(object):
    widgets = attr.ib(init=False, default={})
    widget_set = attr.ib(init=False)

    def addkey(self, tag, *args):
        if tag == 'set':
            self.widget_set.add_key_command(*args)
        else:
            self.widgets[tag]['widget'].add_key_command(*args)

    def add_widget(self, tag, cmd, refresh, text, su, **kwargs):
        self.widgets[tag] = {
            'widget': getattr(self.widget_set, cmd)(**kwargs),
            'refresh': refresh,
            'text': text,
            'type': cmd.partition('_')[2],
            'su': su
        }
        self.widgets[tag]['widget'].set_color(py_cui.GREEN_ON_BLACK)

    def call_cmd(self, tag, cmd, *args, **kwargs):
        if cmd == 'set_text':
            self.widgets[tag]['text'] = ''.join(args)
        elif cmd == 'add_item_list':
            self.widgets[tag]['text'] = args[0]
        elif cmd == 'get':
            return getattr(self.widgets[tag]['widget'], cmd)(*args, **kwargs)
        getattr(self.widgets[tag]['widget'], cmd)(*args, **kwargs)

    def update_SU(self, tag):
        y, x = self.widgets[tag]['widget'].get_absolute_dimensions()
        self.widgets[tag]['su'].update_dim(x - 5, y - 5)

    def clear(self, *args):
        if len(args) == 0:
            for tag in self.widgets:
                if hasattr(self.widgets[tag]['widget'], 'clear'):
                    self.widgets[tag]['widget'].clear()
        else:
            for tag in args:
                if hasattr(self.widgets[tag]['widget'], 'clear'):
                    self.widgets[tag]['widget'].clear()

    def refresh(self):
        for tag in self.widgets:
            if self.widgets[tag]['refresh']:
                self.update_SU(tag)
                wid = self.widgets[tag]
                wid['widget'].clear()
                if wid['type'] == 'text_block':
                    wid['widget'].set_text(wid['su'].format_text(wid['text']))
                elif wid['type'] == 'scroll_menu':
                    wid['widget'].add_item_list(wid['text'])


@attr.s
class MasterScreen(ScreenProcessor, WidgetRing):
    """Class responsible for managing Fetch screen functions.

    Attributes:
        settings (List): list of tuples containing envar and plaintext settings.
        menu_choices (list): list of menu choicefrom overview mode.
    """
    manager: Any = attr.ib(kw_only=True)
    scraper: Any = attr.ib(kw_only=True)
    widget_set = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.widget_set = self.manager.root.create_new_widget_set(10, 8)
        self.widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.show_menu_popup)
        self._check_validation()
        # -------------------------------------------------
        # Widget Set + Info Panel
        # -------------------------------------------------
        self.widget_set.add_key_command(
            py_cui.keys.KEY_M_LOWER,
            self.show_menu,
        )
        self.add_widget(
                'info_panel',
                'add_text_block',
                True,
                '',
                su.StringUtils(x_dim=0, y_dim=0),
                title='Entrez Info',
                row=0,
                column=0,
                row_span=2,
                column_span=2,
                padx=0
        )
        self.update_SU('info_panel')
        self.info_panel = self.widgets['info_panel']

    def initialize_screen_elements(self) -> Any:
        """Function that initializes the widgets for screen."""

    def v1(self):
        if not (isinstance(self.manager, pyentrez.main.entrez_manager.EntrezManager)):
            raise TypeError("manager must be EntrezManager")

    def v2(self):
        if not (isinstance(self.scraper, pyentrez.entrez_scraper.Scraper)):
            raise TypeError("scraper must be Scraper")

    def v3(self):
        if not (isinstance(self.widget_set, py_cui.widget_set.WidgetSet)):
            raise TypeError("widget_set must be WidgetSet")

    def _check_validation(self):
        logger.debug(f'Validating Screen Managers for {self.__class__.__name__}')
        self.v1()
        self.v2()
        self.v3()
