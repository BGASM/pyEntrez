"""Utility module for handling strings."""
import json
import os
import attr
import textwrap
from pathlib import Path
from shutil import copy2 as cp
from typing import List

from loguru import logger
from yaml import dump as dmp
from yaml import safe_load as sl

from pyentrez.utils import envars as ev
from pyentrez.utils import pathloc as pl

stringlist = pl.get_data_path() / 'stringlist.json'
with stringlist.open() as stringfile:
    jdata = json.load(stringfile)

dblist = pl.get_data_path() / 'entrez.json'
with dblist.open() as dbfile:
    dbdata = json.load(dbfile)

r1 = '\n'
r2 = '\n\n'
r3 = '\n\n\n'
t1 = '\t'


@attr.s
class StringUtils(object):
    """Instance used for cases where text wrapping is required, otherwise classmethods are used."""
    x_dim = attr.ib()
    y_dim = attr.ib()
    wrapp: textwrap.TextWrapper() = attr.ib()

    @wrapp.default
    def _wrapp_initialization(self):
        return textwrap.TextWrapper(
            width=self.x_dim,
            max_lines=self.y_dim,
            break_long_words=False,
            break_on_hyphens=False,
        )

    def update_dim(self, x_dim, y_dim):
        """Update xy dimensions of the wrapper."""
        self.wrapp.width = x_dim
        self.wrapp.max_lines = y_dim

    def format_text(self, *args):
        """Reformat text to fit within wrapper dimensions.

        Args:
            *args: text string to be formatted.

        Returns:
            Returns the formatted string.
        """
        text_in = (args[0]).replace('\n\n', '\r').replace('\n', ' ').splitlines()
        return_str = []
        for string in text_in:
            return_str.append(self.wrapp.fill(string + '\n'))
        return r2.join(return_str)

    def get_entrez_help(self) -> str:
        """Parses long string from json file.

        Returns:
            str: Appended and joined string from json file.
        """
        helpstr = []
        for strlist in jdata['HELP']:
            helpstr.append(self.wrapp.fill(r1.join(strlist)))
        return r2.join(helpstr)

    def format_article_list(self, *args):
        """Takes the list of article titles and formats them so each line fits within dimensions.

        Args:
            *args: list of article titles

        Returns:
            Single string with all article titles joined.
        """
        article_list = []
        for article in args[0]:
            article_list.append(self.wrapp.fill(article[1]))
        return r3.join(article_list)

    def get_setting(self) -> str:
        """Parses long string from json file.

        Returns:
            str: Appended and joined string from json file.
        """
        settings = []
        settinglist: Path = pl.get_user_workspace()
        # noinspection PyAugmentAssignment
        settinglist = settinglist / 'my_settings.yaml'
        with open(settinglist, 'r') as sdata:
            settings_dict = sl(sdata)
        for key in settings_dict.items():
            settings.append(f'{key:<15}{str(settings_dict[key])}')
        return r1.join(settings)

    # noinspection PyUnusedLocal
    @staticmethod
    def update_settings(key, value) -> None:
        """Creates a dict of settings set by the user and then sends them to envars."""
        s1: Path = pl.get_user_workspace()
        s2: Path = s1 / 'my_settings.yaml'
        cp(s2, s1 / 'my_settings_backup.yaml')
        pair = {key: value}

        with open(s2, 'r') as file_in:
            in_dict = sl(file_in)
        in_dict.update(pair)
        with open(s2, 'w') as file_out:
            dmp(in_dict, file_out)
        ev.setenv(in_dict)

    
def get_entrez(setting: str) -> List[str]:
    """Returns list of available entrez dbs."""
    logger.info(f'{dbdata}')
    return dbdata.get(setting)


def get_new_path(path) -> str:
    """Accepts path input and returns it."""
    msg = [f'{str(path)} does not exist.', 'Should we create it (Yes, No)?', '.: ']
    return str(input(r1.join(msg)))


def gu_create(switch) -> str:
    """Returns ucreate."""
    if switch == 0:
        jdata['NEWUSR'][0].append(str(pl.uhome()))
        ucreate = ' '.join(jdata['NEWUSR'][0])
    else:
        ucreate = input(r1.join(jdata['NEWUSR'][1]))
    return ucreate


def gu_ow() -> str:
    """Returns Overwrite string."""
    return input(r1.join(jdata['OVERWRITE']))


def get_logo() -> str:
    """Parses long string from json file.

    Returns:
        str: Appended and joined string from json file.
    """
    logo = []
    for strlist in jdata['LOGO']:
        logo.append(strlist)
    return r1.join(logo)


def no_db() -> str:
    """Returns NO_DB string."""
    return input(r1.join(jdata['NO_DB']))


def clear():
    """Uses OS-appropriate clear function in terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


@attr.s
class InteractivePrompt(object):
    """Instance of interactive cmd prompt pyentrez."""
    manager = attr.ib()

    def input(self, script):
        """Takes user input and displays appropriate responses."""
        stringbuff = []
        for strlist in jdata[script]:
            stringbuff.append(strlist)
        clear()
        return input(r1.join(stringbuff))
