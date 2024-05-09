from peewee import SqliteDatabase

from src.config import Config

db = SqliteDatabase(Config.DB_FILENAME)
