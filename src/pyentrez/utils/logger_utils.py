import functools
from typing import Any

from loguru import logger

from pyentrez.utils import pathloc

logpath = pathloc.get_log_path()


def logger_wraps(*, funcentry=True, funcexit=True, level='DEBUG') -> Any:
    """Wrapper that will surround functions, logging entry and exit."""

    def wrapper(func):
        """

        Args:
            func:

        Returns:

        """
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            """

            Args:
                *args:
                **kwargs:

            Returns:

            """
            logger1 = logger.opt(depth=1, colors=True)
            if funcentry:
                logger1.log(level, f"<m><l>Entering '{name}'</></>")
            rst = func(*args, **kwargs)
            if funcexit:
                logger1.log(level, f"<m><l>Exiting '{name}' (result={rst})</></>")
            return rst

        return wrapped

    return wrapper


def close_cleanup() -> None:
    """Function is called when pyEntrez is closed."""
    logger.info('Exiting pyEntrez.')
    logger.info('-----------------------------------------------------')


def clean_exit() -> None:
    """Provides a clean exit with logging and file closing."""
    close_cleanup()
    exit()


def start_logger() -> None:
    """Starts up the loggers."""
    logger.opt(colors=True).info('<g>.......pyEntrez started.......</>')
    logger.add(
        str(logpath / 'trace.log'),
        level='TRACE',
        colorize=False,
        backtrace=False,
        diagnose=False,
        rotation='500 MB',
        format='{message}',
    )
    logger.add(
        str(logpath / 'out_INFO.log'),
        level='INFO',
        colorize=False,
        backtrace=False,
        diagnose=False,
        rotation='500 MB',
        format='{time:YY:MM:DD:HH:mm:ss} |{level} | {message}',
    )
    logger.add(
        str(logpath / 'out_DEBUG.log'),
        level='DEBUG',
        colorize=False,
        backtrace=True,
        diagnose=True,
        rotation='500 MB',
        format='{time:YY:MM:DD:HH:mm:ss} |{level} | {message}',
    )
