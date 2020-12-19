"""Review Screen module contains code for displaying articles.

Entrez requests can be made from here.
Author: William Slattery
Created: 11/24/2020
"""

from typing import Any, Dict, List, Optional, Tuple, Union

import attr
import py_cui
from loguru import logger

# pyEntrez
import pyentrez
from pyentrez import entrez_scraper as SCRAPE
from pyentrez.db import mongo_entrez as MDB
from pyentrez.main import screen_manager as sm
from pyentrez.utils import string_utils as su

# Logger


string_comm = Tuple[Union[str, int], Any]
dict_comm = Dict[Any, List[string_comm]]


@attr.s(slots=True)
class ReviewScreen(sm.MasterScreen):
    """Defines and controls components of the ReviewScreen.

    Inherits from ScreenManager, ScreenProcessor, and WidgetRing.

    Attributes:
        setting_message (str): This string holds whatever value is highlighted when a Py_CUI
            popup is called. Popups only pass newly entered data, but this value is often needed.
        articles (set): This is a two-item set containing PMID and the article Titles.
        paper (set): This is a three-item set containing PMID, Title, and Abstract.

    Slots:
        manager (any): Instance of the top-level EntrezManager.
        setti

    """
    manager: Any = attr.ib(kw_only=True)
    scraper: Any = attr.ib(kw_only=True)
    screen_type = attr.ib(init=False, default='ReviewScreen')
    widget_set = attr.ib(init=False)
    setting_message: Optional[str] = attr.ib(init=False)
    paper: Optional[set] = attr.ib(init=False)
    articles: Optional[set] = attr.ib(init=False)

    def fetch_setting_select(self) -> None:
        """Gets a highlighted string from the menu and toggles.

        The selected string will call a popup box from root_pyCUI.
        Whatever is entered into the prompt box will be sent to the command.

        Attributes:
            self.menu_message (str): We save the string that called. the popup.
            self.toggle_setting (func): popup box will trigger this func.
        """
        self.setting_message = self.call_cmd('article_list', 'get')
        self.manager.root.show_yes_no_popup(
            f'Load article titled: {self.setting_message}',
            self.toggle_setting,
        )

    def toggle_setting(self, msg) -> None:
        """Identify the PMID for selected article Title and requests it from database.

        Compare title substring stored in self.setting_message to all the full title strings
        stored in our self.articles set. On match, pass the PMID to database handler, which will
        return a Set containing the abstract. Send the abstract off to get text_wrapped and then
        set it to the read_panel.

        Args:
            msg (str): String passed
        """
        for article in self.articles:
            if self.setting_message in article[1]:
                self.paper = self.manager.mdb.get_article(article[0])
                text = self.widgets['read_panel']['su'].format_text(self.paper[1])
                self.call_cmd('read_panel', 'set_text', text)
        self.refresh_settings()

    def update_info(self, tag='read_panel', msg='') -> None:
        """Wipes and replaces text on the main info block.

        Args:
            msg (str): String of what needs to be printed on info block.

        ..
        """
        self.clear()
        self.call_cmd(tag, 'set_text', msg)

    def set_initial_values(self) -> None:
        """Function that initializes status bar and initial text for Review screen."""
        self.call_cmd('read_panel', 'set_text', self.widgets['read_panel']['su'].get_entrez_help())
        self.refresh_settings()
        self.manager.root.set_status_bar_text('Settings - Backspace | Quit - q')

    def refresh_settings(self) -> None:
        """Clears and fetches titles of articles held in Database.

        Run a check if application was started with Database functionality, if not it sets
        the string to a standar message informing the user to change their settings.

        If application was started with Database functionality it calls the collect_articles
        function to retrieve the article title set and load it into the instance variable.

        Articles get sent off to be text_wrapped, and then passed to root as a list of strings
        split on newlines.

        Note:
            StringUtils format_article_list accepts the Set of articles, iterates through,
            and concatenates all the titles into a string that gets returned. This instance's
            self.articles Set contains the PMID necessary for requesting abstracts from database.
        """
        wid = self.widgets['article_list']
        if self.collect_articles():
            formatted_articles = wid['su'].format_article_list(self.articles)
        else:
            formatted_articles = su.no_db()
        self.clear('article_list')
        self.call_cmd('article_list', 'add_item_list', formatted_articles.splitlines())

    def collect_articles(self) -> bool:
        """If DB is set up pulls a set of article titles.

        Returns:
            is_db_set (bool): True if the top-level database is set, otherwise False.
        """
        is_db_set = False
        if self.manager.mdb is not None:
            self.articles = self.manager.mdb.get_titles()
            is_db_set = True
        return is_db_set

    def initialize_screen_elements(self) -> Any:
        """Function that initializes the widgets for fetch control screen.

        Returns:
            fetch_screen_widget_set (py_cui.widget_set.WidgetSet):
            Widget set object for fetch control screen.
        """

        # Main reading box
        self.widget_set.add_key_command(
            py_cui.keys.KEY_M_LOWER,
            self.show_menu,
        )
        self.add_widget('read_panel', 'add_text_block', True, '', su.StringUtils(x_dim=0, y_dim=0),
                        title='Entrez Info',
                        row=0,
                        column=4,
                        row_span=10,
                        column_span=4,
                        padx=0
                        )
        self.update_SU('read_panel')
        self.call_cmd('read_panel', 'set_selectable', True)

        # Scrolling block for menu items
        self.add_widget('article_list', 'add_scroll_menu', True, '',
                        su.StringUtils(x_dim=0, y_dim=0),
                        title='Entrez Menu',
                        row=0,
                        column=0,
                        row_span=10,
                        column_span=3,
                        padx=0
                        )
        self.update_SU('article_list')
        self.call_cmd('article_list', 'set_selectable', True)
        self.addkey('article_list',
                    py_cui.keys.KEY_ENTER,
                    self.fetch_setting_select,
                    )
        return self.widget_set
