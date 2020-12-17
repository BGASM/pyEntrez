"""Biopython's Entrez wrapper - provides interface with publication databases.

This module:
    - provide initialization a Scraper
    - create list of supported Entrez databases
    - parse environment settings into correct Entrez args
    - handles logic for constructing Entrez queries
    - handles unpacking Entrez fetch results
"""
import os

import attr
# noinspection PyPep8Naming
# noinspection PyPep8Naming
from Bio import Entrez as ez
from Bio import Medline as ml

from pyentrez.utils import envars as ev


@attr.s
class Scraper(object):
    """Biopython's Entrez Wrapper - facilitates user interface with Entrez.

    Scraper instances will:
        - parse user settings and queries into the appropriate string required
          by Entrez
        - unpack results retruned by Entrez fetches
        - handle WebHistory and complex query language

    Attribues:
        manager (Any): top-level EntrezManager or CmdEntrez making requests
    """

    manager = attr.ib()

    def esearch(self, term):
        """Combines search query and user-defined settings into Entrez-appropriate query.

        esearch assembles query from search term and the params returned based on user's settings.
        Entrez returns its results in a package called 'handle'.
        The handle is unpacked and results are returned as a list of article UID's.

        Args:
            term (str): The term to query in the Entrez database.

        Returns:
             Unpacked dict that contains list of article UID's that match query.
        """
        params = construct_search_params()
        handle = ez.esearch(
            db=os.environ['PYENT_DB'],
            term=term,
            **params,
        )
        uid = ez.read(handle)
        handle.close()
        return uid

    def efetch(self, uid):
        """Comines UID list with user-defined fetch settings to return selected articles.

        efetch assembles query from UID list and the params returned based on user's settings.
        Entrez returns its results in a package called 'handle'.
        The handle is unpacked and results are returned as a dict of articles.
        The dict is packed into a list because MongoDB expects a list of dict objects for bulk
        insertion.

        Args:
            uid (Dict): Contains IdList, which is a list of UID's to return articles for

        Returns:
            List of article dict's to be passed into a user database
        """
        params = construct_fetch_params()
        uid = ','.join(uid['IdList'])
        handle = ez.efetch(
            db=os.environ['PYENT_DB'],
            id=uid,
            **params,
        )
        results = ml.parse(handle)
        results = list(results)
        handle.close()
        return results


def construct_search_params():
    """Iterates through user-defined Entrez Search settings to assemble the search parameters.

    Envars hold the most recent user-defined Entrez settings, such as rettype, retmax, database,
    etc. These settings are iterated through, and their values are returned and appended to the
    query.
    """
    params = {}
    for setting in ev.settings_eSearch:
        if os.environ.get(setting[1]):
            params.update({setting[0].lower(): os.environ.get(setting[1])})
    return params


def construct_fetch_params():
    """Iterates through user-defined Entrez Fetch settings to assemble the search parameters.

    Envars hold the most recent user-defined Entrez settings, such as rettype, retmax, database,
    etc. These settings are iterated through, and their values are returned and appended to the
    query.
    """
    params = {}
    for setting in ev.settings_eFetch:
        if os.environ.get(setting[1]):
            params.update({setting[0].lower(): os.environ.get(setting[1])})
    return params


def define_db(db_name: str):
    """Returns info and parameters expected by the requested Entrez DB."""
    ez.email = os.environ['PYENT_EMAIL']
    handle = ez.read(db=db_name)
    record = ez.read(handle)
    handle.close()
    return record


def update_db_list():
    """Returns available Entrez DB's."""
    ez.email = os.environ['PYENT_EMAIL']
    handle = ez.einfo()
    record = ez.read(handle)
    handle.close()
    return record
