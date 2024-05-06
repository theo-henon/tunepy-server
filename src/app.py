from flask import Flask, request
import bcrypt
from peewee import DoesNotExist

from database.user import User
from database.config import db

# Initialize database connection and tables
db.connect()
db.create_tables([User])

# Initialize flask application
app = Flask(__name__)


@app.route("/users/register", methods=["POST"])
def user_register():
    username, password = None, None
    try:
        username, password = request.json["username"], request.json["password"]
        user_that_may_exists = User.get(User.username == username)
        return {"error": "A user with that username already exists."}, 409
    except KeyError as key_error:
        return {"error": "Missing credentials."}, 400
    except DoesNotExist:
        User.create(username=username, password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()))
        return {"message": f"The user '{username}' has been successfully registered."}, 200


@app.route("/users/login", methods=["POST"])
def user_login():
    # TODO: Return a JWT for user's authentication
    username, password = None, None
    try:
        username, password = request.json["username"], request.json["password"]
        user = User.get(User.username == username)
        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return {"message": f"User '{username}' successfully logged in."}, 200
        else:
            return {"error": "Invalid password."}, 400
    except KeyError as key_error:
        return {"error": "The username or the password is missing"}, 400
    except DoesNotExist as doesnt_exist:
        return {"error": f"The user '{username}' does not exist."}, 404
