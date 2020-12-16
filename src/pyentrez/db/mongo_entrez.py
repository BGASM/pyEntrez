import json
from pathlib import Path
from typing import Any, Optional

import attr
from pymongo import MongoClient as MC

from pyentrez.utils import pathloc as pl

t_host = '127.0.0.1'
t_port = 27017

stringlist = Path(pl.get_db_path() / 'db_files' / 'test_data.json')
with stringlist.open() as stringfile:
    t_dict = json.load(stringfile)


def condense_a(cursor):
    return tuple([cursor['PMID'], cursor['TI']])


def condense_b(cursor):
    return tuple([cursor['PMID'], cursor['AB'], cursor['TI']])


@attr.s
class DBLoader:
    manager: Optional[Any] = attr.ib(default=None)
    host: str = attr.ib(default=t_host)
    port: str = attr.ib(default=t_port)
    d1: str = attr.ib(default='test')
    c1: str = attr.ib(default='articles')
    client: Any = attr.ib(init=False)
    db: Any = attr.ib(init=False)
    coll: Any = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.client = connect_client(self.host, self.port)
        self.db = get_db(self.client, self.d1)
        self.coll = get_coll(self.db, self.c1)

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
        for paper in articles:
            PMID = paper['PMID']
            tmp = self.coll.replace_one(
                {"PMID": PMID},
                paper,
                upsert=True,
            )
            result.append(tmp.upserted_id)
        # result = self.coll.insert_many(articles)
        return result


def connect_client(host, port):
    return MC(host, port)


def get_db(client, db):
    return client[db]


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
