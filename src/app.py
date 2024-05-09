import os

import bcrypt
from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from peewee import DoesNotExist, IntegrityError
from werkzeug.utils import secure_filename

from config import Config
from database.config import db
from database.song import Song
from database.user import User

# Parse configuration file
Config.parse()

# Initialize database connection and tables
db.connect()
db.create_tables([User, Song])

# Initialize flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.API_SECRET_KEY
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)


@app.route("/users/register", methods=["POST"])
def user_register():
    username, password = None, None
    try:
        username, password = request.json["username"], request.json["password"]
        User.create(username=username, password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()))
        return {"msg": f"The user '{username}' has been successfully registered!"}
    except KeyError:
        return {"msg": "Missing credentials."}, 400
    except DoesNotExist:
        return {"msg": f"The user '{username}' has been successfully registered."}, 200
    except IntegrityError:
        return {"msg": "This username is already taken."}, 409


@app.route("/users/login", methods=["POST"])
def user_login():
    username, password = None, None
    try:
        username, password = request.json["username"], request.json["password"]
        user = User.get(User.username == username)
        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            access_token = create_access_token(identity=user.id)
            return {"msg": f"User '{username}' successfully logged in.", "access_token": access_token}, 200
        else:
            return {"msg": "Invalid password."}, 400
    except KeyError:
        return {"msg": "The username or the password is missing"}, 400
    except DoesNotExist:
        return {"msg": f"The user '{username}' does not exist."}, 404


@app.route("/users/profile/<username>", methods=["GET", "PUT"])
@jwt_required()
def user_profile(username):
    if request.method == "GET":
        try:
            user = User.get(User.username == username)
            return {"id": user.id, "username": user.username}
        except DoesNotExist:
            return {"msg": f"User '{username}' not found."}, 404
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
                return {"msg": f"You're not authorized to update {username}'s profile."}, 401
        except DoesNotExist:
            return {"msg": f"User '{username}' not found."}, 404
        except IntegrityError:
            return {"msg": "This username is already taken."}, 409
        except KeyError as key_error:
            pass
        return {"id": user.id, "username": user.username}


@app.route("/songs", methods=["POST"])
@jwt_required()
def post_song():
    song_file = request.files["audio"]
    song_filename = secure_filename(song_file.filename)
    song_path = os.path.join(Config.SONGS_DIRECTORY, song_filename)
    if os.path.exists(song_path) or Song.get_or_none(Song.filename == song_filename) is not None:
        return {"msg": "This file already exists in the server"}, 409
    song_file.save(song_path)
    return {"msg": "The song has been successfully uploaded!"}


if __name__ == "__main__":
    app.run(host=Config.API_HOST, port=Config.API_PORT, debug=Config.DEBUG)
