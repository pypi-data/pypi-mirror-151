import os
import sys
import logging
from typing import Union, NoReturn
from pathlib import Path


log = logging.getLogger(__name__)


def _debugger_is_active() -> bool:
    """Check to see if running in debug mode."""

    gettrace = getattr(sys, "gettrace", lambda: None)
    return gettrace() is not None


def load_dotenv_if_in_debug_mode(env_file: Union[Path, str]) -> NoReturn:
    """
    Load secret .env variables from repo for debugging.

    :param env_file: String or Path like object pointer to secret dot env file to read.
    """

    try:
        from dotenv import load_dotenv
    except ImportError as e:
        log.error(
            """
            Unable to import dotenv.
            Note: The logger should be invoked after reading the dotenv file
            so that the debug level is by the environment.
            """
        )
        log.error(e)
        raise ImportError(
            """
            Unable to import dotenv, is python-dotenv installed?
            Try installing this package using pip install envidat[dotenv].
            """
        )

    if _debugger_is_active():
        secret_env = Path(env_file)
        if not secret_env.is_file():
            log.error(
                """
                Attempted to import dotenv, but the file does not exist.
                Note: The logger should be invoked after reading the dotenv file
                so that the debug level is by the environment.
                """
            )
            raise FileNotFoundError(
                f"Attempted to import dotenv, but the file does not exist: {env_file}"
            )
        else:
            load_dotenv(secret_env)


def get_logger() -> logging.basicConfig:
    """
    Set logger parameters with log level from environment.

    Note: defaults to DEBUG level.
    """

    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", default="DEBUG"),
        format=(
            "%(asctime)s.%(msecs)03d [%(levelname)s] "
            "%(name)s | %(funcName)s:%(lineno)d | %(message)s"
        ),
        datefmt="%y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
    log.debug("Logger set to STDOUT.")
