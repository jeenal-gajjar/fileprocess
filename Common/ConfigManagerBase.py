
import os.path, time, socket, calendar
from Common.Utils import str_to_bool
from configparser import ConfigParser

class ConfigManagerBase(object):

    _instance = None
    filename = ''

    def __init__(self,filepath):
        """ Virtually private constructor. """
        self.fullfilepath = os.path.dirname(filepath)
        self.moduleName = os.path.split(self.fullfilepath)[-1]
        self._configFillePath = '../' + self.moduleName + '/' + self.moduleName + '.conf'
        if ConfigManagerBase._instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.config = ConfigParser()

            self.config.read(self._configFillePath)

    @staticmethod
    def getInstance():
        if ConfigManagerBase._instance == None:
            raise ValueError("ConfigManagerBase instance was not created!")

        return ConfigManagerBase._instance

    def get_host_ip(self):
        self.host_ip  = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

        return self.host_ip

    def get_timestamp(self):
        import datetime
        dt = datetime.datetime.today().replace(hour=13, minute=0, second=0, microsecond=0)
        timestm = str(calendar.timegm(time.gmtime()))
        return timestm

    def get_log_name(self):
        self.log_name = self.config.get('logging', 'log_name')
        return self.log_name


    def get_log_level(self):
        self.LOG_LEVEL = self.config.get('logging', 'log_level')
        lvl ='NOTSET'

        if self.LOG_LEVEL=='DEBUG':
            lvl=10
        elif self.LOG_LEVEL=='WARNING':
            lvl=30
        elif self.LOG_LEVEL=='INFO':
            lvl=20
        elif self.LOG_LEVEL=='NOTSET':
            lvl=0
        elif self.LOG_LEVEL=='ERROR':
            lvl=40
        elif self.LOG_LEVEL=='CRITICAL':
            lvl=50
        else:
            lvl = 0

        return lvl

    def get_log_file(self):
        self.LOG_FILE = self.config.get('logging', 'log_file')
        return self.LOG_FILE

    def get_log_file_maxbytpe(self):
        self.log_file_maxbytpe = self.config.get('logging', 'log_file_maxbytpe')
        inbytes = 1048576 * int(self.log_file_maxbytpe)

        return inbytes

    def get_log_file_numoffile(self):
        self.log_file_numoffile = int(self.config.get('logging', 'log_file_numoffile'))
        return self.log_file_numoffile

    def get_enable_console_handler(self):
        self.enable_console_handler = self.config.get('logging', 'enable_console_handler')
        return str_to_bool(self.enable_console_handler)

    def messageformat(self,msg, status, enable):
        if (enable):
            msg = msg + 'Error:' + status
        return msg

    def get_console_handler_level(self):
        self.console_handler_level = self.config.get('logging', 'console_handler_level')
        return self.console_handler_level

    def get_enable_syslog_handler(self):
        self.enable_syslog_handler = self.config.get('logging', 'enable_syslog_handler')
        return str_to_bool(self.enable_syslog_handler)

    def get_syslog_address(self):
        self.syslog_address = self.config.get('logging', 'syslog_address')
        return self.syslog_address

    def get_syslog_handler_level(self):
        self.syslog_handler_level = self.config.get('logging', 'syslog_handler_level')
        return self.syslog_handler_level

