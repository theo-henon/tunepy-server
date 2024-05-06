from peewee import SqliteDatabase, Model

from database.config import db


class BaseModel(Model):
    class Meta:
        database = db
