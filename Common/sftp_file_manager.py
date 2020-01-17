# Jeenal suthar

from contextlib import ContextDecorator
import pysftp


class SFTPFileManager(ContextDecorator):

    def __init__(self, host, username, private_key, host_key_check=True, remote_path=None):
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
        self.private_key = private_key
        self.connection = None

        self.cnopts = pysftp.CnOpts()
        if not host_key_check:
            self.cnopts.hostkeys = None

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
            self.connection = pysftp.Connection(self.host, username=self.username,
                                                private_key=self.private_key, cnopts=self.cnopts)
            if self.remote_path:
                self.connection.chdir(self.remote_path)

    def change_directory(self, path):
        """
        Change current working directory of remote.

        :param path: remote path
        :return:
        """
        self._make_connection()
        self.connection.chdir(path)

    def create_directory(self, dir_name: str):
        """
        Create remote directory to save backup file
        :return:
        """
        self._make_connection()
        try:
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
        self.connection.get(filename, destination_file_path)

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
