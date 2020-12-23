import json
from pathlib import Path
from typing import Any, Optional
from loguru import logger

import attr
from pymongo import MongoClient as MC
from pymongo.errors import ConnectionFailure
from pyentrez.utils import pathloc as pl


stringlist = Path(pl.get_db_path() / 'db_files' / 'test_data.json')
with stringlist.open() as stringfile:
    t_dict = json.load(stringfile)


def condense_a(cursor):
    return tuple([cursor['PMID'], cursor['TI']])


def condense_b(cursor):
    return tuple([cursor['PMID'], cursor['AB'], cursor['TI']])


@attr.s(auto_attribs=True, kw_only=True)
class DBLoader:
    manager: Optional[Any] = None
    host: Optional[str] = None
    port: Optional[str] = None
    uri: Optional[str] = None
    cloud: bool = False
    d1: str = 'test'
    c1: str = 'articles'
    client: Any = attr.ib(init=False)
    db: Any = attr.ib(init=False)
    coll: Any = attr.ib(init=False)

    def initialize(self):
        logger.debug("Initializing database.")
        if self.cloud:
            self.client = connect_client(self.uri)
        else:
            self.client = connect_client(self.host, self.port)
        try:
            self.client.admin.command('ismaster')
        except ConnectionFailure:
            return 1
        self.db = get_db(self.client, self.d1)
        self.coll = get_coll(self.db, self.c1)
        logger.debug("Database initialized.")
        return 0


    def get_titles(self):
        titles = self.coll.find({}, {"PMID": 1, "TI": 1, "_id": 0})
        title_set = set(map(condense_a, titles))
        return title_set

    def get_article(self, pmid):
        article = self.coll.find({"PMID": pmid}, {"PMID": 1, "TI": 1, "AB": 1, "_id": 0})
        art_set = list(map(condense_b, article))
        return art_set[0]

    def add_many(self, articles):
        result = []
        try:
            self.client.admin.command('ismaster')
        except ConnectionFailure:
            return 1
        for paper in articles:
            PMID = paper['PMID']
            tmp = self.coll.replace_one(
                {"PMID": PMID},
                paper,
                upsert=True,
            )
            result.append(tmp.upserted_id)
        return 0


def connect_client(*args):
    return MC(*args)


def get_db(client, db):
    return client[db]

def list_collections(db):
    return db.list_collection_names()

def get_coll(db, coll):
    return db[coll]


def insert_one(t_coll, document):
    return t_coll.insert_one(document).inserted_id


def test_script():
    client = DBLoader()
    # client.get_titles()
    client.get_article('31116049')


if __name__ == '__main__':
    test_script()
