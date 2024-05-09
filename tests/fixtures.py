import pytest

from app import app, db
from database.user import User


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def clean_database():
    db.drop_tables([User])
    db.create_tables([User])
