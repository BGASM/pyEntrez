"""Module that handles settings and envars.
On initialization this module will create a list of tuples containing the text version of a setting
and its PYENT-envar representation.

Entrez-command-specific formats are created and are callable. (settings_eSearc, etc.)

Sets all the parsed settings to envars
"""
from os import environ as env
from typing import Any, Dict, List, Tuple
from loguru import logger
from pyentrez.utils import variables as vl

# Default envars:
pyenv: List[str] = []
settings: List[Tuple[str, str]] = []
menu = vl.get_settings()
for overall in menu.values():
    for setting in overall:
        if 'setting' in setting.keys():
            pyenv.append(setting['setting']['envar'])
            settings.append((setting['setting']['text'], setting['setting']['envar']))


settings_eSearch: List[Tuple[str, str]] = [
    ('email', 'PYENT_EMAIL'),
    ('usehistory', 'PYENT_USEHISTORY'),
    ('WebEnv', 'PYENT_WEBENV'),
    ('query_key', 'PYENT_QUERYKEY'),
    ('sort', 'PYENT_SORT'),
    ('retmax', 'PYENT_RETMAX'),
    ('retmode', 'PYENT_RETMODE'),
    ('rettype', 'PYENT_RETTYPE'),
    ('field', 'PYENT_FIELD'),
    ('datetype', 'PYENT_DATETYPE'),
    ('reldate', 'PYENT_RELDATE'),
    ('mindate', 'PYENT_MINDATE'),
    ('maxdate', 'PYENT_MAXDATE'),
]

settings_ePost: List[Tuple[str, str]] = [('email', 'PYENT_EMAIL'), ('WebEnv', 'PYENT_WEBENV')]

settings_eSummary: List[Tuple[str, str]] = [
    ('email', 'PYENT_EMAIL'),
    ('WebEnv', 'PYENT_WEBENV'),
    ('query_key', 'PYENT_QUERYKEY'),
    ('retmax', 'PYENT_RETMAX'),
    ('retmode', 'PYENT_RETMODE'),
    ('rettype', 'PYENT_RETTYPE'),
    ('version,', 'PYENT_EZVERSION'),
]

settings_eFetch: List[Tuple[str, str]] = [
    ('email', 'PYENT_EMAIL'),
    ('WebEnv', 'PYENT_WEBENV'),
    ('query_key', 'PYENT_QUERYKEY'),
    ('retmax', 'PYENT_RETMAX'),
    ('retmode', 'PYENT_RETMODE'),
    ('rettype', 'PYENT_RETTYPE'),
]


def setenv(args: Dict[str, Any]) -> None:
    """Function to set envars based on input from CLI argparse.

    Iterates through the passed dict, and for each key it checks
    if it matches any envars. To add more envars, they need to be
    added to cmdline's static default envars variable.

    Args:
        args (dict): dict passed from execute func that has all args from cmd.
    """
    for key2 in pyenv:
        tmp_str = (key2.split('_')[1]).lower()
        if tmp_str in args.keys():
            env[key2] = str(args[tmp_str])
        else:
            env[key2] = 'None'
