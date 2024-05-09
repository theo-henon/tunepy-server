from fixtures import *


def test_register(client):
    register_response = client.post("/users/register", json={
        "username": "pytest",
        "password": "pytest"
    })
    assert register_response.status_code == 200
    assert register_response.json["msg"] == "The user 'pytest' has been successfully registered!"
