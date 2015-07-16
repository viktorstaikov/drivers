# models
from peewee import *


class Driver(Model):
    name = CharField(unique=True)
    email = CharField(unique=True)
    status = IntegerField(
        choices=((0, 'not checked'), (1, 'clean'), (2, 'discrepancy in docs'), (3, 'fake documents')), default=0)
