"""
Database configuration file.
"""

import peewee as pw

_DB = None
_DB_HOSTS = None
_DB_NAME = None


def get_db():
    """
    Return database connection object.
    :return:
    """
    global _DB
    return _DB


def set_db(config):
    """
    Take config object as parameter, get database info from config
    and configure database connection object.

    :param config:
    :return:
    """

    global _DB, _DB_NAME, _DB_HOST
    _DB_NAME = config.get_db_name()
    _DB_HOST = config.get_db_host()

    _DB = pw.MySQLDatabase(
        _DB_NAME,
        user=config.get_db_username(),
        password=config.get_db_password(),
        host=_DB_HOST,
    )
    return _DB

