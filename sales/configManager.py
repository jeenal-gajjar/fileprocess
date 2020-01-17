import os
from Common.ConfigManagerBase import  ConfigManagerBase
from Common.db.config_manager import DbConfigManager
from Common.Utils import create_directory, delete_directory_tree
from time import gmtime, strftime


class ConfigManager(ConfigManagerBase, DbConfigManager):
    __instance = None

    def __init__(self):
        self.filepath = __file__
        self._date_format_prefix = None
        self._local_directory = None
        self._working_directory = None
        self._destination_directory = None
        self._data_provider_name = None
        self._last_process_file_name = None
        self._data_provider_settings = None
        self._backup_directory = "backup"
        super().__init__(self.filepath)

    @staticmethod
    def getInstance():

        """ Static access method. """
        if ConfigManagerBase._instance == None:
            raise ValueError("ConfigManagerHelper instance was not created!")

        return ConfigManagerBase._instance

    @staticmethod
    def createInstance():

        """ Static access method. """
        if ConfigManagerBase._instance == None:
            ConfigManagerBase._instance = ConfigManager()
        return ConfigManagerBase._instance

    def get_datepattern(self):
        startwith_date_pattern = self.config.get('main', 'date_format_prefix')
        return strftime(startwith_date_pattern, gmtime())

    def get_local_directory(self):
        if not self._local_directory:
            self._local_directory = self.config.get('main', 'local_directory')
            if self._local_directory is '':
                raise ValueError(f"Local Directory Path does not mentioned in conf file")
            if not os.path.exists(self.config.get('main', 'local_directory')):
                create_directory(self.config.get('main', 'local_directory'))
        return self._local_directory

    def get_working_directory(self):
        if not self._working_directory:
            self._working_directory = self.config.get('main', 'working_directory')
            if self._working_directory == '':
                raise ValueError(f"Working Directory Path does not mentioned in conf file")
            if not os.path.exists(self.config.get('main', 'working_directory')):
                create_directory(self.config.get('main', 'working_directory'))
        return self._working_directory

    def get_destination_directory(self):
        if not self._destination_directory:
            self._destination_directory = self.config.get('main', 'destination_directory')
            if self._destination_directory is '':
                raise ValueError(f"Destination Directory Path does not mentioned in conf file")
            if not os.path.exists(self.config.get('main', 'destination_directory')):
                create_directory(self.config.get('main', 'destination_directory'))
        return self._destination_directory

    def get_backup_directory(self):
        if not self._backup_directory:
            self._backup_directory = self.config.get('main', 'backup_directory')
        return self._backup_directory

    def get_destination_file_path(self,file):
        self.destination_directory = self.get_destination_directory()
        return os.path.join(self.destination_directory, file)

    def get_profile_builder_conf(self):
        return self.config.get('main', 'profile_builder_conf')

    def get_data_file_prefix(self):
        return self.config.get('main', 'data_file_prefix')

    def get_date_format_prefix(self):
        if not self._date_format_prefix:
            self._date_format_prefix = self.config.get('main', 'date_format_prefix')
        return self._date_format_prefix

    def get_data_provider_name(self):
        if not self._data_provider_name:
            self._data_provider_name = self.config.get('main', 'data_provider_name')
        return  self._data_provider_name

    def get_data_file_extension(self):
        return  self.config.get('main', 'data_file_extension')

    def get_sftp_enabled(self):
        return self.config.getboolean('main', 'sftp_enable')

    def get_encryption_enable(self):
        return self.config.getboolean('main', 'encryption_enable')

    def get_sftp_host(self):
        self.sftp_host = self.config.get('sftp_server', 'sftp_host')
        return self.sftp_host

    def get_sftp_username(self):
        self.sftp_username = self.config.get('sftp_server', 'sftp_username')
        return self.sftp_username

    def get_sftp_data_private_key(self):
        self.sftp_data_private_key = self.config.get('sftp_server', 'sftp_data_private_key')
        return self.sftp_data_private_key

    def get_remote_data_directory(self):
        self.remote_data_directory = self.config.get('sftp_server', 'remote_data_directory')
        return self.remote_data_directory

    def get_email_subject(self):
        return self.config.get('email', 'subject')

    def get_receiver_email(self):
        return self.config.get('email', 'receiver_email')

    def get_sender_email(self):
        return self.config.get('email', 'sender_email')

    def get_password(self):
        return self.config.get('email', 'password')

    def get_smtp_server(self):
        return self.config.get('email', 'smtp_server')

    def get_port(self):
        return self.config.get('email', 'port')

    def get_last_process_file_name(self):
        self._last_process_file_name = self.config.get('main', 'last_process_file_name')
        return self._last_process_file_name

    def get_data_provider_settings(self):
        if not self._data_provider_settings:
            data_provider_name = self.config.get('main', 'data_provider_name')
            data_provider_section_name = data_provider_name
            self._data_provider_settings = dict(self.config.items(data_provider_section_name))
        return self._data_provider_settings




