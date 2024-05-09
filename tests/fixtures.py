import pytest

from app import app, db
from database.user import User


@pytest.fixture
def test_reset_app():
    app.config.update({"TESTING": True})
    yield app
    db.drop_tables([User])
    db.create_tables([User])


@pytest.fixture
def client(test_reset_app):
    return app.test_client()


@pytest.fixture
def runner(test_reset_app):
    return app.test_cli_runner()
