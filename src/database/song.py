from peewee import AutoField, CharField, DateTimeField, ForeignKeyField

from database.base_model import BaseModel
from database.user import User


class Song(BaseModel):
    id = AutoField()
    uploader = ForeignKeyField(model=User, null=False)
    upload_date = DateTimeField(null=False)
    filename = CharField(null=False, unique=True)
