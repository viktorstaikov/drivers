from flask_peewee.rest import RestAPI, Authentication, RestResource
from models import Driver
from drivers import app
import json

public_auth = Authentication(protected_methods=[])

# instantiate public api for the data
api = RestAPI(app, default_auth=public_auth)
api.register(Driver)
api.setup()


@app.route('/api/export/driver', methods=['GET'])
def export_drivers():
    drivers = Driver.select(
        Driver.id, Driver.name).dicts().execute().cursor.fetchall()
    return json.dumps(drivers)
