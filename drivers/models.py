# models
from peewee import *
from datetime import datetime


class Driver(Model):
    name = CharField(unique=True)
    email = CharField(unique=True)
    telnumber = CharField(default='')
    address = CharField(default='')
    car = CharField(default='')
    status = IntegerField(
        choices=((0, 'not checked'), (1, 'clean'), (2, 'discrepancy in docs'), (3, 'fake documents')), default=0)
    lastmodified = DateTimeField(default=datetime.now, null=False)
