# all the imports
import json
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from contextlib import closing

# configuration
# DATABASE = 'hello.db'
# DEBUG = True
# SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
# app.config.from_object(__name__)


# def connect_db():
#     return sqlite3.connect(app.config['DATABASE'])

from drivers.db_adapter import connect_db


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


import drivers.routes
import drivers.api

if __name__ == '__main__':
    app.debug = True

    app.run()
