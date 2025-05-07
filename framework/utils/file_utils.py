import logging
import os
import shutil
import time
from pathlib import Path
from typing import Union

from framework.constants.timeouts import Timeouts

logger = logging.getLogger(__name__)


def is_file_exist(file_path: Union[Path, str], timeout: int = Timeouts.WAIT_FILE_DOWNLOAD) -> bool:
    """
    Check whether the file exists within the timeout.
    """
    logger.info(f"Check if file '{file_path}' exists.")

    try:
        wait_for_file_exists(file_path, timeout)
        return True
    except TimeoutError as err:
        logger.info(err)
        return False


def remove_dir_if_exist(path: Union[Path, str]) -> None:
    """
    Remove a directory and all its contents.
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def wait_for_file_exists(file_path: Union[str, Path], timeout: int = Timeouts.WAIT_FILE_DOWNLOAD,
                         polling_interval: int = Timeouts.POLLING_INTERVAL) -> None:
    """
    Wait until a file exists within the given timeout.

    :param file_path: Path to the file (as string or Path).
    :param timeout: Maximum time to wait in seconds.
    :param polling_interval: Time between checks in seconds.
    :raises TimeoutError: If the file does not appear within the timeout.
    """
    file_path = Path(file_path)
    logger.debug(f"Waiting for file '{file_path}' to exist...")

    end_time = time.time() + timeout
    while time.time() < end_time:
        if file_path.exists():
            logger.debug(f"File '{file_path}' found.")
            return
        time.sleep(polling_interval)

    raise TimeoutError(f"File '{file_path}' did not exist within {timeout} seconds.")
