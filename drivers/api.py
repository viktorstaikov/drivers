from flask_peewee.rest import RestAPI, Authentication, RestResource
from flask import make_response, request
from models import Driver
from drivers import app
from datetime import datetime
import json

ALLOWED_EXTENSIONS = ['csv']

public_auth = Authentication(protected_methods=[])

# instantiate public api for the data
api = RestAPI(app, default_auth=public_auth)
api.register(Driver)
api.setup()


@app.route('/api/export/driver', methods=['GET'])
def export_drivers():
    drivers = Driver.select(
        Driver.id, Driver.name).dicts().execute().cursor.fetchall()
    csv = ''

    for driver in drivers:
        csv += str(driver[0]) + ',' + driver[1] + '\n'

    response = make_response(csv)

    response.headers[
        "Content-Disposition"] = "attachment; filename=drivers-unchecked.csv"
    return response


def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/api/import/driver', methods=['GET', 'POST'])
def import_background_checks():
    f = request.files['file']
    if f and allowed_extension(f.filename):
        content = f.read()
        tokens = content.split('\n')

        clean = []
        discrepancy = []
        fake = []
        for token in tokens:
            subtokens = token.split(',')
            if len(subtokens) == 3:
                id = subtokens[0]
                name = subtokens[1]
                status = int(subtokens[2])

                if status == 1:
                    clean.append(id)
                elif status == 2:
                    discrepancy.append(id)
                elif status == 3:
                    fake.append(id)

        print(str(clean))

        now = datetime.now

        Driver.update(status=1, lastmodified=datetime.now).where(
            Driver.id << clean).execute()
        Driver.update(status=2, lastmodified=datetime.now).where(
            Driver.id << discrepancy).execute()
        Driver.update(status=3, lastmodified=datetime.now).where(
            Driver.id << fake).execute()

        drivers = Driver.select(
            Driver.id, Driver.name, Driver.status).where(Driver.lastmodified > now).dicts().execute().cursor.fetchall()
        return make_response(str(drivers))
    return make_response("nope")
