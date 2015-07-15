from flask_peewee.rest import RestAPI, Authentication
from models import Driver
from drivers import app

# create a RestAPI container
# api = RestAPI(app)

# instantiate our api wrapper, specifying user_auth as the default
api = RestAPI(app, default_auth=Authentication(protected_methods=[]))

# register the Driver model
api.register(Driver)

api.setup()
