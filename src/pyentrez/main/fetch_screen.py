"""This is the main screen that is initialized when starting pyEntrez.

Entrez requests can be made from here.
Author: William Slattery
Created: 11/24/2020
"""

import os
from typing import Any, Dict, List, Optional, Tuple, Union

import attr
import py_cui
from loguru import logger

# pyEntrez
import pyentrez
from pyentrez import entrez_scraper as SCRAPE
from pyentrez.main import screen_manager as sm
from pyentrez.utils import envars as ev
from pyentrez.utils import logger_utils as lu
from pyentrez.utils import logic
from pyentrez.utils import string_utils as su

# Logger


string_comm = Tuple[Union[str, int], Any]
dict_comm = Dict[Any, List[string_comm]]


@attr.s(slots=True)
class FetchScreen(sm.MasterScreen):
    """Class responsible for managing Fetch screen functions.

    Attributes:
        settings (List): list of tuples containing envar and plaintext settings.
        menu_choices (list): list of menu choicefrom overview mode.
    """
    manager: Any = attr.ib(kw_only=True)
    scraper: Any = attr.ib(kw_only=True)
    screen_type = attr.ib(init=False, default='Fetch Screen')
    widget_set = attr.ib(init=False)

    def fetch_setting_select(self) -> None:
        """Gets a highlighted string from the menu and toggles.

        The selected string will call a popup box from root_pyCUI.
        Whatever is entered into the prompt box will be sent to the command.

        Attributes:
            self.menu_message (str): We save the string that called. the popup.
            self.toggle_setting (func): popup box will trigger this func.
        """
        self.setting_message = self.call_cmd('setting_box', 'get')
        self.manager.root.show_text_box_popup(
            f'Reset setting: Currently {self.setting_message}',
            self.toggle_setting,
        )

    def toggle_setting(self, msg) -> None:
        """Swaps the envar value for msg.

        A setting is called from the menu_box and a popup prompt called.

        Args:
            msg (str): String passed
        """
        menu: List[str] = self.setting_message.split(' ')
        for setting in ev.get_settings():
            if setting[0] == menu[0]:
                error, err = logic.fetch_check(setting[0], msg)
                if not error:
                    os.environ.pop(setting[1])
                    os.environ[setting[1]] = str(msg)
                    break
                else:
                    self.manager.root.show_warning_popup('Invalid Setting', err)
                    break
        self.refresh_settings()

    def query(self) -> None:
        """Submits query to configured db."""
        query_message = self.call_cmd('query_box', 'get')
        self.clear('query_box')
        uid = self.scraper.esearch(query_message)
        results = self.scraper.efetch(uid)
        ids = self.manager.mdb.add_many(results)

    def update_info(self, tag='info_panel', msg='') -> None:
        """Wipes and replaces text on the main info block.

        Args:
            msg (str): String of what needs to be printed on info block.

        ..
        """
        self.clear()
        if tag == 'info_panel' and msg == '':
            self.call_cmd(tag, 'set_text', self.widgets[tag]['su'].get_entrez_help())
        else:
            self.call_cmd(tag, 'set_text', msg)

    def set_initial_values(self) -> None:
        """Function that initializes status bar for Fetch screen."""
        self.call_cmd('info_panel', 'set_text', self.widgets['info_panel']['su'].get_entrez_help())
        self.refresh_settings()
        self.manager.root.set_status_bar_text('Settings - Backspace | Quit - q')

    def refresh_settings(self) -> None:
        """Clears and resets Fetch widgets.

        Right now this only refreshes the menu box, but we should expand this
        to refresh all widgets or make the def more specific.
        The importance here is that the with pyCUI the str that is displayed in
        a menu box is often also the command passed.

        """
        out = []
        for setting in ev.settings:
            tmp_str = [setting[0], os.getenv(setting[1], default='')]
            out.append(' : '.join(tmp_str))
            out.append('\n')
        msg: str = ''.join(out)
        self.clear('setting_box')
        self.call_cmd('setting_box', 'add_item_list', msg.splitlines())

    def initialize_screen_elements(self) -> Any:
        """Function that initializes the widgets for fetch control screen.

        Returns:
            fetch_screen_widget_set (py_cui.widget_set.WidgetSet):
            Widget set object for fetch control screen.
        """
        # Widget Set
        self.widget_set.add_key_command(
            py_cui.keys.KEY_M_LOWER,
            self.show_menu,
        )
        self.add_widget('query_box', 'add_text_box', False, '', None,
                        title='Entrez Query',
                        row=9,
                        column=0,
                        column_span=8,
                        )
        self.call_cmd('query_box', 'set_focus_text', 'Submit Query - Enter | Return - Esc')
        self.call_cmd('query_box', 'set_selectable', True)
        self.addkey('query_box',
                    py_cui.keys.KEY_ENTER,
                    self.query,
                    )
        # Main info text block listing information for all pyEntrez operations
        self.add_widget('info_panel', 'add_text_block', True, '', su.StringUtils(x_dim=0, y_dim=0),
                        title='Entrez Info',
                        row=0,
                        column=4,
                        row_span=9,
                        column_span=4,
                        padx=0
                        )
        self.update_SU('info_panel')
        self.call_cmd('info_panel', 'set_selectable', True)

        # Scrolling block for menu items
        self.add_widget('setting_box', 'add_scroll_menu', True, '',
                        su.StringUtils(x_dim=0, y_dim=0),
                        title='Entrez Menu',
                        row=0,
                        column=0,
                        row_span=8,
                        column_span=2,
                        padx=0
                        )
        self.update_SU('setting_box')
        self.call_cmd('setting_box', 'set_selectable', True)
        self.addkey('setting_box',
                    py_cui.keys.KEY_ENTER,
                    self.fetch_setting_select,
                    )
        return self.widget_set
