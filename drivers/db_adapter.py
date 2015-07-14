import sqlite3
from drivers import app

# configuration
DATABASE = 'hello.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
