from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import bcrypt
from peewee import DoesNotExist

from database.user import User
from database.config import db

# Initialize database connection and tables
db.connect()
db.create_tables([User])

# Initialize flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_strong_secret_key'
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)


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
    username, password = None, None
    try:
        username, password = request.json["username"], request.json["password"]
        user = User.get(User.username == username)
        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            access_token = create_access_token(identity=user.id)
            return {"message": f"User '{username}' successfully logged in.", "access_token": access_token}, 200
        else:
            return {"error": "Invalid password."}, 400
    except KeyError as key_error:
        return {"error": "The username or the password is missing"}, 400
    except DoesNotExist as doesnt_exist:
        return {"error": f"The user '{username}' does not exist."}, 404


@app.route("/users/profile/<username>", methods=["GET", "PUT"])
@jwt_required()
def user_profile(username):
    if request.method == "GET":
        try:
            user = User.get(User.username == username)
            return {"id": user.id, "username": user.username}
        except DoesNotExist as doesnt_exist:
            return {"error": f"User '{username}' not found."}, 404
    else:
        user_id = get_jwt_identity()
        user = None
        try:
            user = User.get(User.username == username)
            if user.id == user_id:
                new_username = request.json["username"]
                user.username = new_username
                user.save()
            else:
                return {"error": f"You're not authorized to update {username}'s profile."}, 401
        except DoesNotExist as doesnt_exist:
            return {"error": f"User '{username}' not found."}, 404
        except KeyError as key_error:
            pass
        return {"id": user.id, "username": user.username}
