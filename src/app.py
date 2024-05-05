from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<name>")
def hello_user(name):
    return render_template("hello.html", name=name)
