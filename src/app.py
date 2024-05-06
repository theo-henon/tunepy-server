from flask import Flask, render_template

from database.user import User
from database.config import db

# Initialize database connection and tables
db.connect()
db.create_tables([User])

# Initialize flask application
app = Flask(__name__)
