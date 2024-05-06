from peewee import AutoField, CharField

from database.base_model import BaseModel


class User(BaseModel):
    id = AutoField()
    username = CharField()
    password = CharField()
