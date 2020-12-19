# -*- coding: utf-8 -*-
"""Top-level module for pyentrez.

This module:
    - initializes logging
    - allows configuring logging
    - tracks version of pyentrez

"""
import sys
from importlib.metadata import distribution as dist
from pathlib import Path
from typing import Any

from loguru import logger

distro = dist('pyentrez')
__version__ = str(distro.version)
__licence__ = str(distro.metadata['License'])
__copyright__ = f'Copyright (c) 2020 {distro.metadata["Author"]}'

# Logger initialization
LOG_FORMAT = '{time:YY:MM:DD:HH:mm:ss} |{level} | {message}'
_VERBOSITY_TO_LOG_LEVEL = {
    1: 'INFO',
    2: 'DEBUG',
    3: 'TRACE',
}


def configure_logger(verbosity, filename=None, format=LOG_FORMAT) -> None:
    """Configure logging for pyentrez.log

    Args:
        verbosity (int): How verbose the logging should be.
        filename (str): Path logs should be saved to.
        format (str): Custom logging format.
    """
    if verbosity <= 0:
        return
    if verbosity > 3:
        verbosity = 3
    log_level = _VERBOSITY_TO_LOG_LEVEL[verbosity]
    if not filename or filename in ('stderr', 'stdout'):
        fileobj = getattr(sys, filename or 'stderr')
    else:
        fileobj = filename

    logger.add(
        fileobj,
        level=log_level,
        colorize=False,
        backtrace=True,
        diagnose=True,
        rotation='500 MB',
        format=LOG_FORMAT,
    )
