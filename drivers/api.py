from flask_peewee.rest import RestAPI, Authentication, RestResource
from flask import make_response
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
    csv = 'ID, Name\n'

    for driver in drivers:
        csv += str(driver[0]) + ',' + driver[1] + '\n'

    response = make_response(csv)

    response.headers[
        "Content-Disposition"] = "attachment; filename=drivers-unchecked.csv"
    return response
