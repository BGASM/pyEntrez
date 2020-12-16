"""CMD is main entry into script.

Checks if it is user's first time running script. Creates the argparser.
Interpret whether to run pyEntrez in cmd or tui mode. Create setting dir
for new user. Set all the envars for script.
"""

# Core Python Utils
from os import environ as env
from pathlib import Path
from shutil import copy2 as cp
from shutil import rmtree as rt
from typing import Any, Dict, List, Optional, Tuple, Union

# Logger
# YAML Utility
from yaml import dump as dmp
from yaml import safe_load as sl

# pyEntrez
from pyentrez.utils import logic as lg
from pyentrez.utils import pathloc as pl
from pyentrez.utils import string_utils as su

check_path = Union[Path, bool]
drs = ['settings', 'data', 'pyEntrez', 'config']
cfg = Path(pl.get_config_path())
rootdirs = {'defconf': (cfg / 'default_config.yaml'), 'coreconf': (cfg / 'core_config.yaml')}


def first_run() -> None:
    """Create workspace dir if user's first time using script.

    Called if there is no user directory set up for the user's USERNAME envar.
    User prompted to enter a workspace directory otherwise default.
    Creates directory structure.
    Directories are created with a 755 setting: wrx for user, r for all others.
    Sets PYENT_HOME envar to the root PyEntrez directory set up.
    Pass user data to cfg_user_add function, to update the core config file

    .. todo:: Expand exception handling
    """
    fwd = False
    while fwd is False:
        print(su.StringUtils.gu_create(0))
        npth: str = lg.three_arg_sel(su.StringUtils.gu_create(1), str(pl.uhome()), '')  # noqa: WPS221
        npth = npth.split(drs[2])[0]
        path: Path = Path(npth) / drs[2]
        if lg.path_set(path):
            fwd = lg.test_bool(su.StringUtils.gu_ow(), 'FORCE')
            rt(path, ignore_errors=True)
        else:
            fwd = True
    # noinspection PyUnboundLocalVariable
    makedirs(path)


def makedirs(path: Path) -> None:
    """Make the user directory.

    Args:
        path (pathlib): root path to the user's workspace
    """
    p1: List[Path] = [(path / drs[0]), (path / drs[1])]
    for pth in p1:
        pth.mkdir()
    env['PYENT_HOME'] = str(path)
    cfg_user_add(p1[0])


def cfg_user_add(p1: Path) -> None:
    """Add USERNAME and settings path to core_config file for script startup.

    The core_config.yaml file needs to be located in the config dir on the
    script install path.
    New users are added as key:value pairs with envar USERNAME as key,
    and settings dir as value.
    defpaths[0] = core_config.yaml
    defpaths[1] = default_config.yaml
    defpaths[2] = user's settings dir

    Args:
        p1 (path): Abs path to user's settings directory.
    """
    usr = {env['USERNAME']: str(p1)}
    cp(rootdirs['defconf'], (p1 / 'my_settings.yaml'))
    users_dict = safe_open_file(rootdirs['coreconf'])
    users_dict['USER_CFG'].update(usr)
    out = safe_write_file(rootdirs['coreconf'], users_dict)


def get_usr_path() -> Tuple[bool, check_path]:
    """Function may be used to return the user's setting directory path.

    Verify if a user is a first time user or not via check_new().
    This is done by checking core_config and using envar USERNAME as a key,
    looking for a directory value.
    If the user is new, or if there is no valid setting path the return True
    (syntax calling is: first_use, path = get_usr_path)
    If the user is a returning user and the search shows a valid
    USERNAME: dir_path pair, then FALSE and the path are returned.

    Returns:
        bool:   first_time True if no USERNAME:path_to_settings in core_config
        Union[bool, Path]:   If this is user's first time using script False
    """
    path: check_path = False
    first_time = False
    user_dict = safe_open_file(rootdirs['coreconf'])
    if env['USERNAME'] in user_dict['USER_CFG']:
        path = Path(user_dict['USER_CFG'][env['USERNAME']])
        env['PYENT_HOME'] = str(path)
    else:
        first_time = True
    return first_time, path


def safe_write_file(path: Path, users_dict) -> Any:
    with open(path, 'w') as file2:
        return dmp(users_dict, file2)


def safe_open_file(path: Path) -> Dict[str, Any]:
    with open(path) as file1:
        return sl(file1)


# noinspection PyUnusedLocal
def check_new() -> Path:
    """Check if a user setting directory has been created for the user.

    Checks if a user directory has been created for the user.
    User is defined by envar USERNAME.
    If first run, call the functions to create a workspace.
    When the loop succeeds (checkingUser = False) returns the user path.

    Returns:
        path(pathlib): user's my_settings.yaml path.
    """
    return_path: Optional[Path] = None
    path: check_path = False
    checkinguser: bool = True
    while checkinguser is True:
        first, path = get_usr_path()
        if first or not path:
            first_run()
        else:
            if isinstance(path, Path):  # noqa: WPS513
                return_path = path
                checkinguser = False
    assert return_path is not None
    return return_path
