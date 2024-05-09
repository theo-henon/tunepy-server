from peewee import AutoField, CharField

from database.base_model import BaseModel


class User(BaseModel):
    id = AutoField(primary_key=True)
    username = CharField(unique=True)
    password = CharField()
