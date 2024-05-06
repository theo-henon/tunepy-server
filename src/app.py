from flask import Flask, render_template

from database.user import User
from database.config import db

# Initialize database connection and tables
db.connect()
db.create_tables([User])

# Initialize flask application
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<name>")
def hello_user(name):
    return render_template("hello.html", name=name)
