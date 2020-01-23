# Created By:       Jeenal Suthar
# Created Date:
# Last Modified:    22/01/2020
# Description:      This Module Provide the implementation of logging Manager .

from contextlib import contextmanager, ContextDecorator
from functools import wraps
import time
import logging
import logging.handlers
from Common.ConfigManagerBase import ConfigManagerBase
configManager =ConfigManagerBase.getInstance()

from Common.Utils import get_os_login

class UTCFormatter(logging.Formatter):
    """
    the implementation of UTC logging formatter class.
    """
    converter = time.gmtime


def _create_logger(log_file, logger_name, filemaxbytes, backupcount, loglevel,host_ip
                   ,enable_syslog_handler,syslog_address,syslog_handler_level,enable_console_handler,
                   console_handler_level) ->logging.Logger:


    """
    Helper function to create logger with the defined configurations
    :param log_file:
    :param logger_name:
    :param filemaxbytes:
    :param backupcount:
    :param loglevel:
    :return:
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(loglevel)

    # create a file handler
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=filemaxbytes,  backupCount=backupcount)
    handler.setLevel(loglevel)

    # create a logging format
    formatter = UTCFormatter('%(levelname)s - %(asctime)s - %(name)s - %(process)d - %(thread)d -'+ host_ip+'- %(message)s ]')
    handler.setFormatter(formatter)
    if enable_syslog_handler:

        hndl = logging.handlers.SysLogHandler(address=syslog_address)
        formatter = logging.Formatter('- %(levelname)s - %(name)s - 01_700 - %(process)d - '   + get_os_login()+' - '+host_ip+' - %(message)s ')
        hndl.setFormatter(formatter)
        hndl.setLevel(syslog_handler_level)
        logger.addHandler(hndl)

    if enable_console_handler:
        hndlst = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s ')

        hndlst.setFormatter(formatter)
        hndlst.setLevel(console_handler_level)
        logger.addHandler(hndlst)

    logger.addHandler(handler)
    return logger


_logger = _create_logger(configManager.get_log_file(), configManager.get_log_name(),
                         configManager.get_log_file_maxbytpe(), configManager.get_log_file_numoffile(),
                         configManager.get_log_level(),configManager.get_host_ip(),
                         configManager.get_enable_syslog_handler(),configManager.get_syslog_address(),
                         configManager.get_syslog_handler_level(),configManager.get_enable_console_handler(),
                         configManager.get_console_handler_level())


def get_applogger() -> logging.Logger:
    """
    Return a pre-configured logger object for the application
    :return:
    """
    return _logger

def get_applogger_update() -> logging.Logger:
    """
    Return a pre-configured logger object for the application
    :return:
    """
    _logger_update = _create_logger(configManager.get_LOG_FILE(), configManager.get_LOG_NAME(),
                                    configManager.get_LOG_FILE_MAXBYTPE(),
                                    configManager.get_LOG_FILE_NUMOFFILE(),
                                    configManager.get_LOG_LEVEL(), configManager.get_HOST_IP(),
                                    configManager.get_enable_syslog_handler(),
                                    configManager.get_syslog_address(),
                                    configManager.get_syslog_handler_level(),
                                    configManager.get_enable_console_handler(),
                                    configManager.get_console_handler_level())

    return _logger_update

class LogManager(ContextDecorator):
    """
    This is the LogManager responsible for providing logging functionality to code blocks as ContextManager.
    It allows logging code block entry and exit in addition to logging exception.

    :param str name:
    :param bool tracing: Log block enter exit debug logger
    :param bool error_log: logger exceptions if any
    :param bool reraise_except: if logger exception is enabled, then flag to decide to re-raise or not
    :return: None
    """

    __slots__ = ["name", "tracing", "error_log", "reraise_except", "log_error_func"]

    def __init__(self, name=None, tracing=True, error_log=True, reraise_except=True, log_error_as_fatal=False):
        self.name = name
        self.tracing = tracing
        self.error_log = error_log
        self.reraise_except = reraise_except
        self.log_error_func = _logger.error if log_error_as_fatal else _logger.critical

    def __enter__(self):
        if self.name and self.tracing:
            _logger.debug("Enter:"+self.name)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_val:
            # you need to always re-raise if error logging is not enabled
            if self.error_log:
                if not (issubclass(exc_type, SystemExit) and exc_val.code == 0):
                    if self.name:
                        self.log_error_func('Error in:' + self.name, exc_info=(exc_type, exc_val, exc_tb))
                    else:
                        self.log_error_func('Error', exc_info=(exc_type, exc_val, exc_tb))

                if self.reraise_except:
                    return False  # reraise the exception
                else:
                    return True  # suppress the exception
            else:
                return False  # reraise the exception
        else: # no exception, then just logger block exit if requested
            if self.name and self.tracing:
                _logger.debug("Exit:" + self.name)


class TraceManager(LogManager):
    """
    This is a responsible for providing logging functionality that traces the code block entry exit event as ContextManager.
    This is a specialized LogManager yet it ignore exceptions.
    """
    def __init__(self, name=None):
        super().__init__(name, error_log=False, reraise_except=False)


@contextmanager
def log_manager(name=None, tracing=True, error_log=True, reraise_except=True):
    """
    this is the main log_manager responsible for providing logging functionality to code blocks. It allows logging
    code block entry and exit in addition to logging exception.

    :param str name:
    :param bool tracing: Log block enter exit debug logger
    :param bool error_log: logger exceptions if any
    :param bool reraise_except: if logger exception is enabled, then flag to decide to re-raise or not
    :return: None
    """

    try:
        if name and tracing:
            _logger.debug("Enter:"+name)
        yield None
    except:
        # you need to always re-raise if error logging is not enabled
        if error_log:
            if name:
                _logger.error('Error in:' + name, exc_info=True)
            else:
                _logger.error('Error', exc_info=True)
            if reraise_except:
                raise
        else:
                raise
    else:
        if name and tracing:
            _logger.debug("Exit:"+name)


@contextmanager
def trace_manager(name=None):
    """
    A Tracing only logger manager, only logging code block enter/exit event
    :param name: Code block name; possibly function name.
    :return:
    """
    yield log_manager(name, tracing=True, error_log=False)


def logging_wrapper(f):
    """
     A decorator to wrap and logger exceptions
    :param f:
    :return:
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        """
        wrappers the context manager to handle
        exception logging
        :param args:
        :param kwargs:
        :return:
        """
        with log_manager(f.__name__):
            return f(*args, **kwargs)
    return wrapper
