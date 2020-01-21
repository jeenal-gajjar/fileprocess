# Created By:       Jeenal Suthar
# Created Date:
# Last Modified:    22/01/2020
# Description:      This Module Provide Peewee Model .

import peewee as pw
from Common.db import base

class Product(base.BaseModel):
    """
        Model for Product.
     """
    name = pw.CharField(max_length=250)
    category = pw.CharField(max_length=250)
    description = pw.CharField(max_length=250)
    room_id = pw.IntegerField()
    location_id = pw.CharField(max_length=250)
