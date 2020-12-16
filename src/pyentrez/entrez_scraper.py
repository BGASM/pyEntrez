import os

import attr
# noinspection PyPep8Naming
# noinspection PyPep8Naming
from Bio import Entrez as ez
from Bio import Medline as ml

from pyentrez.utils import envars as ev


@attr.s
class Scraper(object):
    """Biopython's Entrez."""

    manager = attr.ib()

    @staticmethod
    def _construct_search_params():
        params = {}
        for setting in ev.get_settings_eSearch():
            if os.environ.get(setting[1]):
                params.update({setting[0].lower(): os.environ.get(setting[1])})
        return params

    @staticmethod
    def _construct_fetch_params():
        params = {}
        for setting in ev.get_settings_eFetch():
            if os.environ.get(setting[1]):
                params.update({setting[0].lower(): os.environ.get(setting[1])})
        return params

    def esearch(self, term):
        # esearch needs to be passed db, term, **kewyds
        params = self._construct_search_params()
        handle = ez.esearch(
            db=os.environ['PYENT_DB'],
            term=term,
            **params,
        )
        uid = ez.read(handle)
        handle.close()
        return uid

    def efetch(self, uid):
        params = self._construct_fetch_params()
        uid = ','.join(uid['IdList'])
        handle = ez.efetch(
            db=os.environ['PYENT_DB'],
            id=uid,
            **params,
        )
        results = ml.parse(handle)
        results = list(results)
        return results

    '''
    def test(self, db: str, term: str, **keywds):
        logger.info(f'{db}\n{term}\n{keywds}')
        return 'fake uid'
    '''

    @staticmethod
    def define_db(db_name: str):
        ez.email = os.environ['PYENT_EMAIL']
        handle = ez.einfo(db=db_name)
        record = ez.read(handle)
        return record

    @staticmethod
    def update_db_list():
        ez.email = os.environ['PYENT_EMAIL']
        handle = ez.einfo()
        record = ez.read(handle)
        handle.close()
        return record
