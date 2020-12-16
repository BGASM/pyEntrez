from typing import Any, Dict

import attr
# Logger
from loguru import logger

# This is where we will import all sub-component modules
from pyentrez import entrez_scraper as SCRAPE
from pyentrez.db import mongo_entrez as MDB
from pyentrez.utils import logger_utils as lu
from pyentrez.utils import string_utils as su

logger.opt(colors=True)
manager_dict = Dict[str, Any]


@attr.s
class CommandEntrez(object):
    """Placeholder."""
    scrape = attr.ib(default=None)
    mdb = attr.ib(default=None)
    prompt = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.scrape = SCRAPE.Scraper(self)
        self.mdb = MDB.DBLoader(self)
        self.prompt = su.InteractivePrompt(self)

    def query(self):
        query = self.prompt.input('QUERY')
        uid = self.scrape.esearch(query)
        results = self.scrape.efetch(uid)
        ids = self.mdb.add_many(results)
        for i in ids:
            print(f'{i}')

    def start(self):
        """Initiates opening ANY window."""
        task = self.prompt.input('NOTUI_WELCOME')
        if task.isdigit():
            if int(task) == 1:
                self.query()
        else:
            lu.clean_exit()
