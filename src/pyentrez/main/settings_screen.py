"""Settings Screen reads currently loaded settings and allows permanent or on the fly changes.
"""
# pyEntrez
# noinspection PyUnresolvedReferences
from typing import Any, List, Optional, Tuple

import attr
import py_cui
from loguru import logger

import pyentrez
from pyentrez import entrez_scraper as SCRAPE
from pyentrez.main import screen_manager as sm
from pyentrez.utils import envars as ev
from pyentrez.utils import logic
from pyentrez.utils import string_utils as su


# Logger


@attr.s(slots=True)
class SettingsScreen(sm.MasterScreen):
    """Class for settings subscreen in pyEntrez."""

    manager: Any = attr.ib(kw_only=True)
    scraper: Any = attr.ib(kw_only=True)
    screen_type = attr.ib(init=False, default='Settings Screen')
    widget_set = attr.ib(init=False)

    def settings_select(self) -> None:
        """Gets a highlighted string from the menu and toggles.

        The selected string will call a popup box from root_pyCUI.
        Whatever is entered into the prompt box will be sent to the command.

        Attributes:
            self.menu_message (str): We save the string that called. the popup.
            self.toggle_setting (func): popup box will trigger this func.
        """
        self.setting_message = self.call_cmd('settings_menu', 'get')
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
        if msg.isdigit():
            msg = int(msg)
        su.update_settings(menu[0], msg)
        self.refresh_status()

    def initialize_screen_elements(self):
        """Function that initializes the widgets for fetch control screen.

        Returns:
            settings_screen_widget_set (py_cui.widget_set.WidgetSet):
            Widget set object for fetch control screen.
        """
        # Info Panel
        self.widget_set.add_key_command(
            py_cui.keys.KEY_M_LOWER,
            self.show_menu,
        )
        self.add_widget('settings_menu', 'add_scroll_menu', True, '',
                        su.StringUtils(x_dim=0, y_dim=0),
                        title='Settings Menu',
                        row=2,
                        column=4,
                        row_span=7,
                        column_span=2,
                        )
        self.update_SU('settings_menu')
        self.call_cmd('settings_menu', 'set_selectable', True)
        self.addkey('settings_menu',
                    py_cui.keys.KEY_ENTER,
                    self.settings_select,
                    )
        # Logo and link labels
        self.add_widget('logo_label', 'add_block_label', False, su.get_logo(), None,
                        title='Logo Label',
                        row=0,
                        column=0,
                        row_span=2,
                        column_span=3,
                        center=True,
                        )
        self.call_cmd('logo_label', 'set_color', py_cui.RED_ON_BLACK)
        self.add_widget('link_label', 'add_label', False, 'Settings Screen - pyEntrez', None,
                        title='Settings Screen - pyEntrez',
                        row=0,
                        column=3,
                        row_span=2,
                        column_span=3,
                        )
        self.call_cmd('link_label', 'add_text_color_rule', 'Settings Screen*',
                      py_cui.CYAN_ON_BLACK,
                      'startswith',
                      match_type='line',
                      )
        return self.widget_set

    def refresh_status(self) -> None:
        """Clears and resets Fetch widgets.

        Right now this only refreshes the menu box, but we should expand this
        to refresh all widgets or make the def more specific.
        The importance here is that the with pyCUI the str that is displayed in
        a menu box is often also the command passed.

        """
        self.clear()
        self.call_cmd('settings_menu', 'add_item_list',
                      self.widgets['settings_menu']['su'].get_setting().splitlines())

    def clear_elements(self):
        """Placeholder."""
        self.clear()

    def set_initial_values(self) -> None:
        """Function that initializes status bar for Fetch screen."""
        self.call_cmd('settings_menu', 'add_item_list',
                      self.widgets['settings_menu']['su'].get_setting().splitlines())
        self.manager.root.set_status_bar_text('Settings - Backspace | Quit - q')

