# all the imports
import sqlite3
from flask import Flask, request, session, g, abort
from contextlib import closing
from flask_peewee.db import Database
from models import Driver

# create our little application :)
app = Flask(__name__)
app.config.from_object('drivers.config')

# instantiate the db wrapper
db = Database(app)


import drivers.routes
import drivers.api_new
