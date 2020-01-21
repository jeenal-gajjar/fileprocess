# Created By:       Jeenal Suthar
# Created Date:
# Last Modified:    22/01/2020
# Description:      This Module Provide Peewee Base Model .


from playhouse.signals import Model

from Common.db import get_db


class BaseModel(Model):
    """
    Base class for peewee models which provide connection object.
    """

    class Meta:
        database = get_db()

