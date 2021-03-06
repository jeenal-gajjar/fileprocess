# Created By:       Jeenal Suthar
# Created Date:
# Last Modified:    22/01/2020
# Description:      This module get file form remote directory or from local directory.

import os
import shutil
from shutil import move
from Common.Utils import create_directory
from Common.sftp_file_manager import SFTPFileManager
from Common.logging.loggingManager import  get_applogger
_log = get_applogger()

class FileFetchManager():

    _sftpFileManager = None

    def __init__(self, config):
        self.config = config
        self._abs_dir = None
        self.sftp_enable = self.config.get_sftp_enabled()

        if self.sftp_enable:
            self._sftpFileManager = SFTPFileManager(self.config.get_sftp_host(), self.config.get_sftp_username(),
                                                    self.config.get_sftp_password())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.sftp_enable:
            if self._sftpFileManager:
                self._sftpFileManager.close()

    def list_dir(self, remote_dir=None):
        if self.sftp_enable:
            return self._sftpFileManager.list_dir(self.config.get_remote_data_directory())
        else:
            return os.listdir(self.config.get_local_directory())

    def get_file(self, remote_path, local_path):
        if self.sftp_enable:
            self._sftpFileManager._make_connection()
            if self._sftpFileManager.connection:
                self._sftpFileManager.connection.get(remote_path, local_path, preserve_mtime=True)
        else:
            shutil.copy(remote_path, local_path)

    def file_info(self, file_name):
        file_path = self.get_file_path(file_name)
        if self.sftp_enable:
            if self._sftpFileManager.connection:
                return self._sftpFileManager.connection.stat(file_path)
        else:
            return os.stat(file_path)

    def close(self):
        if self.sftp_enable:
            if self._sftpFileManager:
                self._sftpFileManager.close()

    def get_file_path(self, file_name):
        if self.sftp_enable:
            if self._sftpFileManager:
                return self.config.get_remote_data_directory() + '/' + file_name
        else:
            return self.config.get_local_directory() + '/' + file_name

    def create_backup_directory(self):
        if self._abs_dir:
            return self._abs_dir
        else:
            if self.sftp_enable:
                if self._sftpFileManager:
                    self._abs_dir = self.config.get_remote_data_directory() + '/' + self.config.get_backup_directory()
                    self._sftpFileManager.create_directory(self._abs_dir)
            else:
                self._abs_dir = os.path.join(self.config.get_local_directory(), self.config.get_backup_directory())
                create_directory(self._abs_dir)
            return self._abs_dir


    def generate_backup_file(self, file_name):
        return self._abs_dir + '/' + file_name

    def move_file(self, source_file_path, backup_file_path):
        if self.sftp_enable:
            if self._sftpFileManager:
                self._sftpFileManager.move_file(source_file_path, backup_file_path)
        else:
            move(source_file_path, backup_file_path)
