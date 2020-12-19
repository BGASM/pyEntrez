"""Handles complex logic functions that don't need to be explicitly stated in other places."""
from pathlib import Path
from typing import Tuple

from loguru import logger

from pyentrez import exceptions
from pyentrez.utils import string_utils as su


def fetch_check(setting: str, change: str) -> Tuple[bool, str]:
    """Verifies queries sent to eFetch."""
    error: bool = False
    err: str = ''
    if setting == 'Retmax':
        if not change.isdigit():
            error = True
            err = 'Retmax must be a integer.'
    elif setting == 'DB':
        dbsettings = 'Placeholder'
        if not any((dbsetting == change) for dbsetting in dbsettings):
            error = True
            err = f'{change} is not a valid database.'
    return error, err


def three_arg_sel(arg1: str, arg2: str, test: str) -> str:
    """Pass in two args and a test, if arg1 != test return arg2.

    Args:
        arg1 (var): arg to be tested
        arg2 (var): arg to return if arg1 fails
        test (var): test

    Returns:
        arg2 (var): if arg1 is not test
    """
    return arg2 if arg1 == test else arg1


def test_bool(arg1, test) -> bool:
    """Pass in two args and a test, if arg1 != test return arg2.

    Args:
        arg1 (var): arg to be tested
        test (var): test

    Returns:
        True (bool): if arg1 is test
    """
    return arg1.lower() == test.lower()


# noinspection PyTypeChecker
def path_set(path: Path) -> bool:
    """Checks  path for existance and permissions and tries to make the path.

    Args:
        path (pathlib): path that needs to be vetted

    Returns:
        tryagain (bool): True stops calling function, False allows to continue.
    
    Raises:
        CleanExit: If no path set this enables application to exit.
    """
    tryagain = True
    access: int = 0o755
    if path.exists():
        tryagain = True
    else:
        md = su.get_new_path(path)
        if md.lower() == 'yes' or 'y':
            try:
                path.mkdir(mode=access)
            except OSError as error:
                logger.error(f'{error}')
            tryagain = False
        else:
            raise exceptions.CleanExit()
    return tryagain
