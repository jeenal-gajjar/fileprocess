import os
import shutil
import time
import random
from datetime import datetime, timezone
from enum import Enum
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

def getFileName(filePath:str):
    """
    Returns the file name from the fiven path
    :param filePath:
    :return:
    """

    #return filePath.split("\\")[len(__file__.split("\\")) - 1]
    return os.path.basename(filePath)

def remove_file(file, logger):
    try :
        os.remove(file)
    except Exception as e:
        if logger is not None:
            logger.error(e)


def is_dir(file):

    return os.path.isdir(file)


_pid = None
def get_pid():
    global _pid
    if _pid == None:
        try:
            _pid = os.getpid()
        except:
            ts = int(time.time())
            rand = random.randint(1, 101)
            _pid=str(ts) + str(rand)

    return _pid


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

def get_file_modified_time(path: str):
    return datetime.fromtimestamp(os.path.getmtime(path))


class CompressionAlgorithm(Enum):
    """
    Supported Compression Types
    """
    gz = 1
    xz = 2


def compress_file(in_file_name: str, out_file_name: str, algorithm:CompressionAlgorithm=CompressionAlgorithm.gz):
    """
    Compress the given file using gzip
    :param in_file_name: Input full file name to compress
    :param out_file_name: Output full file name (compressed file name)
    :param algorithm: Required compression Algorithm, Default to gz.
    :return:
    """
    if algorithm == CompressionAlgorithm.gz:
        _compress_file_gz(in_file_name, out_file_name)
    elif algorithm == CompressionAlgorithm.xz:
        if in_file_name.endswith(".gz"):
            _compress_file_gz_to_xz(in_file_name, out_file_name)
        else:
            _compress_file_xz(in_file_name, out_file_name)
    else:
        raise ValueError(f"Invalid Compression Algorithm argument value{algorithm if algorithm is None else 'None'}")


def _compress_file_gz(in_file_name: str, out_file_name: str):
    """
    Compress the given file using gzip
    :param in_file_name: Input full file name to compress
    :param out_file_name: Output full file name (compressed file name)
    :return:
    """
    import gzip
    import shutil

    with open(in_file_name, 'rb') as f_in:
        with gzip.open(out_file_name, 'wb', compresslevel=6) as f_out:
            shutil.copyfileobj(f_in, f_out)


def _compress_file_xz(in_file_name: str, out_file_name: str):
    import lzma
    import shutil

    with open(in_file_name, 'rb') as f_in:
        with lzma.LZMAFile(out_file_name, preset=3, mode="wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def _compress_file_gz_to_xz(in_file_name: str, out_file_name: str):
    import gzip
    import lzma
    import shutil
    with gzip.open(in_file_name, "rb") as f_in:
        with lzma.LZMAFile(out_file_name, preset=3, mode="wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


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


