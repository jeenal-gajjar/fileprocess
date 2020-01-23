# Created By:       Jeenal Suthar
# Created Date:
# Last Modified:    22/01/2020
# Description:      This module get file form remote directory.

from contextlib import ContextDecorator
import pysftp
from Common.logging.loggingManager import  get_applogger
_log = get_applogger()

class SFTPFileManager(ContextDecorator):

    def __init__(self, host, username, Password, remote_path=None):
        """
        Initialize sftp connection.

        :param host: host name where to connect.
        :param username: username for connection
        :param private_key: password of user account
        :param host_key_check: flag, sftp check host key of server.
        :param remote_path: path where to upload files.
        """
        self.remote_path = remote_path
        self.host = host
        self.username = username
        self.password = Password
        self.connection = None


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _make_connection(self):
        """
        Initialise connection to sftp server. if not already connected.
        And change current directory if given.

        :return:
        """
        if not self.connection:

            try:
                if self.host and self.username and self.password:
                    self.connection = pysftp.Connection(self.host, username=self.username, password=self.password
                                                       )
                    if self.remote_path:
                        self.connection.chdir(self.remote_path)
            except Exception as e:
                _log.error("[ SFTPFileManager -> _make_connection ] " + str(e))

    def change_directory(self, path):
        """
        Change current working directory of remote.

        :param path: remote path
        :return:
        """
        self._make_connection()
        if self.connection:
            self.connection.chdir(path)

    def create_directory(self, dir_name: str):
        """
        Create remote directory to save backup file
        :return:
        """
        self._make_connection()
        try:
            if  self.connection:
                self.connection.makedirs(dir_name)
        except FileExistsError:
            pass

    def upload_file(self, filename, remote_path=None):
        """
        Upload file to remote server. on given remote path.

        :param filename: file name which send to store.
        :param remote_path: remote path where to upload file, if none default path will use
        :return:
        """
        self._make_connection()
        if self.connection:
            if remote_path:
                self.connection.put(filename, remotepath=remote_path)
            else:
                self.connection.put(filename)

    def list_dir(self, remote_dir=None):
        """
        Returns list of files name exists in remote directory.

        :return:
        """
        self._make_connection()
        if self.connection:
            if remote_dir:
                return self.connection.listdir(remote_dir)
            else:
                return self.connection.listdir()

    def download_file(self, filename, destination_file_path):
        """
        Download given file from remote directory, and save it on given path.

        :param filename:
        :param destination_file_path:
        :return:
        """
        self._make_connection()
        if self.connection:
            self.connection.get(filename, destination_file_path)

    def move_file(self, filename, destination_file_path):
        """
            Move file to remote server. on given remote path.
           :param filename: file name which send to store.
           :param remote_path: remote path where to move file, if none default path will use
           :return:
        """
        self._make_connection()
        if self.connection:
            if destination_file_path:
                self.connection.rename(filename, destination_file_path)
            else:
                self.connection.rename(filename)


    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
