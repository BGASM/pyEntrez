"""Main entry into script.

Global logging settings configured here, including primary sink
definitions. Calls the execute function from pyEntrez commandline
module.
"""
import sys
from typing import List, Optional

from loguru import logger

from pyentrez.main import cmdline


def main(argv=None):
    """Execute the main application.

    Creates instance of cmdline, runs it, and exits the application.
    Args:
        argv(List[str]): Arguments to be passed into the application for parsing.
    """
    if sys.version_info > (3, 8):
        cmd = cmdline.CLI()
        cmd.execute()
        cmd.clean_exit()

    else:
        raise Exception('Script needs to be run with Python 3.8')
