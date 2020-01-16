from contextlib import ContextDecorator

import os
from logging import Logger
from uuid import uuid4

from Common.Utils import create_directory, delete_directory_tree
from Common.decorators.singletonDecorator import Singleton


@Singleton
class WorkingDirectoryManager(ContextDecorator):
    """
    A Context Manager class that create a working/temporary directory for the process upon entry and remove the entire
    directory along with all its contents upon exit.
    """
    def __init__(self, logger: Logger, root_dir: str):

        if not os.path.exists(root_dir):
            raise ValueError(f"Creating Working Directory failed. {root_dir} directory does not exist")
        self._logger = logger
        self._root_dir = root_dir
        self._current_working_dir = os.path.join(self._root_dir, str(uuid4()))

    def __enter__(self):
        self._logger.debug(f"Creating Working Directory {self._current_working_dir}")
        create_directory(self._current_working_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._logger.debug(f"Deleting Working Directory {self._current_working_dir}")
            delete_directory_tree(self._current_working_dir, self._logger)
        except Exception as e:
            pass

    def create_directory(self, dir_name: str):
        abs_dir = os.path.join(self._current_working_dir, dir_name)
        create_directory(abs_dir)
        return abs_dir

    def get_directory_path(self, dir_name: str):
        return os.path.join(self._current_working_dir, dir_name)

    @property
    def path(self):
        return self._current_working_dir



