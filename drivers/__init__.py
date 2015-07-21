# all the imports
from flask import Flask
from flask_peewee.db import Database


# create our little application :)
app = Flask(__name__)
app.config.from_object('drivers.config')


# instantiate the db wrapper
db = Database(app)


from models import Driver


if Driver.table_exists() == False:
    Driver.create_table()
    Driver.create(username='admin@admin.com', email='admin@admin.com',
                  password='admin', is_admin=True, name='Admin')


import drivers.routes
import drivers.api
