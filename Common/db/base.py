# Jeenal suthar

from playhouse.signals import Model

from Common.db import get_db


class BaseModel(Model):
    """
    Base class for peewee models which provide connection object.
    """

    class Meta:
        database = get_db()

