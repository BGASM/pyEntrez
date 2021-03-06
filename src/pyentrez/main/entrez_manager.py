"""This contains code for main interface between application components.

Active role is handling instancing of different screens, switching between screens, and
calling for their refresh on resize events from root.

Passively, this module handles and passes instances of Database Client and the Entrez Scraper.

Author: Will Slattery
Created: 11/23/2020
"""

import os
from typing import Any, Dict, Optional
import subprocess
import threading
import attr
# Logger
from loguru import logger
import asyncio

# This is where we will import all sub-component modules
import pyentrez
from pyentrez import entrez_scraper as SCRAPE
from pyentrez.db import mongo_entrez as MDB
from pyentrez.main import fetch_screen as FETCH
from pyentrez.main import review_screen as REVIEW
from pyentrez.main import settings_screen as SETTINGS
from pyentrez.utils import string_utils as su

# Main pyEntrez manager class
logger.opt(colors=True)
manager_dict = Dict[str, Any]


@attr.s
class EntrezManager(object):
    """This is the main interface between the TUI Screens and functional modules.

    Instances of this class initialize and manage all TUI screens as well as functional packages
    such as Database Client and the Entrez Scraper. They also handle calling for screen refreshes
    when top-level refresh_height_width hook is called.

    Args:
        root (py_cui.PyCUI): Instance of top-level PyCUI allowing for lower-level ScreenManagers to
            make calls to up to root. This is how widgets will add key commands, layout, and text.

    Attributes:
        root (py_cui.PyCUI): Instance of top-level PyCUI.
        mgr (Dict[str, Any]): Contains instances of all Screen classes.
        widget (Dict[str, Any]): Contains instances of each Screen's WidgetSet.
        scrape (Scraper): Instance of Entrez Scraper to be passed into FetchScreen.
        current_state (str): What state the application is in, initialization or current screen.
    """

    root = attr.ib()
    current_state = attr.ib(default='Initialization')
    mgr = attr.ib(default={})
    widget = attr.ib(default={})
    scrape = attr.ib()
    mdb = attr.ib()
    db_set = attr.ib(init=False, default = False)
    operation_thread = attr.ib(init=False)
    # -------------------------------------------------
    # Start of Initialization functions
    # -------------------------------------------------
    @scrape.default
    def _scraper_initialization(self):
        return SCRAPE.Scraper(self)

    @mdb.default
    def _mdb_initialization(self):
        db = None
        if (os.environ.get('PYENT_MONGO')) == 'True':
            if os.environ.get('PYENT_CLOUD') == 'True':
                logger.info(f'Cloud-based Mongo client. URI: {os.environ.get("PYENT_URI")}')
                db = MDB.DBLoader(manager=self,
                                  cloud=True,
                                  uri=os.environ.get('PYENT_URI'),
                )
            else:
                logger.info(f'Local Mongo client. Host: {os.environ.get("PYENT_HOST")}'
                             f'  PORT: {os.environ.get("PYENT_PORT")}')
                db = MDB.DBLoader(manager=self,
                                  cloud=False,
                                  host=os.environ.get('PYENT_HOST'),
                                  port=int(os.environ.get('PYENT_PORT')),
                )
        return db

    def _manager_initialization(self):
        return {
            'FETCH': FETCH.FetchScreen(manager=self, scraper=self.scrape),
            'SET': SETTINGS.SettingsScreen(manager=self, scraper=self.scrape),
            'REVIEW': REVIEW.ReviewScreen(manager=self, scraper=self.scrape),
        }

    def _widget_initialization(self):
        return {
            'FETCH': self.mgr['FETCH'].initialize_screen_elements(),
            'SET': self.mgr['SET'].initialize_screen_elements(),
            'REVIEW': self.mgr['REVIEW'].initialize_screen_elements(),
        }

    def _validate_managers(self):
        pass

    def __attrs_post_init__(self):
        self.mgr.update(self._manager_initialization())
        self.widget.update(self._widget_initialization())
        self.open_window('FETCH')

    # -------------------------------------------------
    # End of Initialization functions
    # -------------------------------------------------
    def perform_long_operation(self, title, long_operation_function, post_loading_callback):
        """Function that wraps an operation around a loading icon popup.

        Args:
        title (str): title for loading icon
        long_operation_function (Any): operation to perform in the background
        post_loading_callback (Any): Function fired once long operation is finished.
        """

        logger.info(f'Executing long operation {title}')
        self.root.show_loading_icon_popup('Please Wait', title, callback=post_loading_callback)
        self.operation_thread = threading.Thread(target=long_operation_function)
        self.operation_thread.start()

    def load_db(self):
        """Load the database."""
        logger.debug("Loading database.")
        out = None
        err = 0
        if self.mdb.initialize() == 1:
            out = 'Mongo Client failed to connect.'
            err = 1
            logger.debug("Database failed to load")
        else:
            out = "Mongo Client connected!"
            self.db_set = True
            logger.debug("Database loaded")
        return out, err

    def fetch_query(self, results):
        """Load the database."""
        logger.debug("Fetching query.")
        out = None
        err = 0
        if self.mdb.add_many(results) == 1:
            out = 'Mongo Client failed to connect.'
            err = 1
            logger.debug("Database failed to load")
        else:
            out = "Query Fetched!"
            logger.debug("Database loaded")
        return out, err

    def refresh_h_w(self):
        """Calls for Screen instances to refresh widgets on a terminal resize event.

        This function is called when the Py_CUI root responds to a terminal resize event.
        On a terminal resize, Py_CUI resizes the widget borders, but not the text inside.
        This function calls for Screens to run their text-wrapping functions.
        """
        for mgr in self.mgr.items():
            self.mgr[mgr].refresh()

    def open_window(self, manager: str) -> None:
        """Directs Py_CUI root which widget_set to apply.

        Clears the widget_set of the existing manager using current_state, then
        initializes the called manager and sends it to the Py_CUI root.

        Args:
            manager(str): The name of which Widget manager to pass to root.
        """
        if self.current_state != 'Initialization':
            self.mgr[self.current_state].clear_elements()
        self.mgr[manager].set_initial_values()
        self.root.apply_widget_set(self.widget[manager])
        self.root.set_title(f'pyEntrez v{pyentrez.__version__} {manager}')
        self.current_state = manager


