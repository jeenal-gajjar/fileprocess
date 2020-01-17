# Jeenal suthar
import os
import shutil
from datetime import datetime, timezone
from logging import Logger


def get_os_login():
    try:

        return os.getlogin()
    except:
        return ""

def utctime():
    """
    Return current time in UTC in in seconds since the epoch as a interger number
    :return:
    """
    # return datetime.now(timezone.utc).timestamp()
    datetime.utcnow()
    return int(datetime.now().timestamp())

def utcdatetime():
    """
    Return current date time in UTC
    :return:
    """
    return datetime.now(timezone.utc)

def str_to_bool(value:str):
    TRUE_STRINGS = ["TRUE", "T", "YES", "Y", "1"]

    if value.upper() in TRUE_STRINGS:
        return True
    else:
        return False

def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def delete_directory_tree(dir_name: str, logger: Logger):
    try:
        shutil.rmtree(dir_name)
    except FileNotFoundError:
        pass
    except Exception as e:
        if logger is not None:
            logger.error(e)


def create_directory(dir_name: str):
    """
    Create destination directory to save file and temporary directory.
    :return:
    """
    try:
        os.makedirs(dir_name)
    except FileExistsError:
        pass


def str_to_list(value: str, delimiter: str):
    """
    Converts the given delimiter separated string into list
    :param value: delimiter separated string
    :param delimiter: delimiter char
    :return: List of the delimited values
    """
    return list(map(str.strip, value.split(delimiter)))

class FileFetchException(Exception):
    pass


