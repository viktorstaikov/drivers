# models
from peewee import *
from flask_peewee.auth import BaseUser
from datetime import datetime
from drivers import db


class Driver(db.Model, BaseUser):
    # for auth purpose
    active = BooleanField(default='True')
    username = CharField(unique=True, null=False)
    password = CharField(null=False)
    is_admin = BooleanField(default='False')

    # custom fields
    name = CharField(unique=True)
    email = CharField(unique=True)
    telnumber = CharField(default='')
    address = CharField(default='')
    car = CharField(default='')
    status = IntegerField(
        choices=((0, 'not checked'), (1, 'clean'), (2, 'discrepancy in docs'), (3, 'fake documents')), default=0)
    lastmodified = DateTimeField(default=datetime.now, null=False)

    # methods
    def check_password(self, password):
        return self.password == password
