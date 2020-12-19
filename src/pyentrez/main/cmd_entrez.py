"""Module for the interactive cmd prompt"""
from typing import Any, Dict

import attr
# Logger
from loguru import logger

# This is where we will import all sub-component modules
from pyentrez import entrez_scraper as SCRAPE
from pyentrez.db import mongo_entrez as MDB
from pyentrez.utils import string_utils as su

logger.opt(colors=True)
manager_dict = Dict[str, Any]


@attr.s
class CommandEntrez(object):
    """Interactive commandline prompt implementation of pyentrez.

    Attributes:
        scrape (Any): scrape is the scraper from the top-level
        mdb (Any): mdb is the top-level database being used
        prompt (Any): instance of StringUtils interactive prompt
    """
    scrape = attr.ib(default=None)
    mdb = attr.ib(default=None)
    prompt = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.scrape = SCRAPE.Scraper(self)
        self.mdb = MDB.DBLoader(self)
        self.prompt = su.InteractivePrompt(self)

    def query(self):
        """Handles parsing a query and printing UID's.

        Calls for the prompt to print the response for a query and returns the user's input.
        The user's input is sent through esearch, which returns a handle. That handle is parsed,
        the UID's and articles attached to them are added to the database, and the list of UID's
        are printed.
        """
        query = self.prompt.input('QUERY')
        uid = self.scrape.esearch(query)
        results = self.scrape.efetch(uid)
        ids = self.mdb.add_many(results)
        for i in ids:
            print(f'{i}')

    def start(self):
        """Initializes a prompt and waits for user input.

        If user input matches query it runs the query routine. Otherwise it does nothing,
        allowing the app to exit.
        """
        # TODO: setup functions for other user options
        task = self.prompt.input('NOTUI_WELCOME')
        if task.isdigit():
            if int(task) == 1:
                self.query()
