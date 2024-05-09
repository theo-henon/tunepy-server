import datetime
from peewee import AutoField, CharField, DateTimeField, ForeignKeyField

from database.base_model import BaseModel
from database.user import User


class Song(BaseModel):
    id = AutoField()
    uploader = ForeignKeyField(model=User, null=False)
    upload_date = DateTimeField(null=False, default=datetime.datetime.now())
    filename = CharField(null=False, unique=True)
