"""Module holds absolute paths to installation directory."""

from importlib import resources as impr
from os import environ as env
from pathlib import Path

with impr.path(__package__, 'pathloc.py') as filepath:
    bottompath = filepath


def get_user_workspace() -> Path:
    """Return absolute path to user settings dir

    Data is loaded into envars on initialization
    """
    pth: Path = Path(env.get('PYENT_HOME'))
    return pth


def get_util_path() -> Path:
    """Returns absolute path to util dir.

    Returns:
        Path: Abs path to /util.
    """
    bot: Path = bottompath.resolve()
    return bot.parent


def get_root_path() -> Path:
    """Returns absolute path to rot dir.

    Returns:
        Path: Abs path to /pyentrez.
    """
    return get_util_path().parent


def get_config_path() -> Path:
    """Returns absolute path to config dir.

    Returns:
        Path: Abs path to /config.
    """
    tmp: Path = get_root_path()
    return tmp / 'config'


def get_log_path() -> Path:
    """Returns absolute path to logs dir.

    Returns:
        Path: Abs path to /logs.
    """
    tmp: Path = get_root_path()
    return tmp / 'logs'


def get_data_path() -> Path:
    """Returns absolute path to logs dir.

    Returns:
        Path: Abs path to /logs.
    """
    tmp: Path = get_root_path()
    return tmp / 'data'


def get_db_path() -> Path:
    """Returns absolute path to logs dir.

    Returns:
        Path: Abs path to /logs.
    """
    tmp: Path = get_root_path()
    return tmp / 'db'


def uhome() -> Path:
    """Simple function to return root dir."""
    return Path.home()
