from flask_peewee.rest import RestAPI, Authentication, UserAuthentication, RestResource
from flask_peewee.auth import Auth
from flask import make_response, request
from peewee import IntegrityError
from models import Driver
from drivers import app, db
from datetime import datetime
import json


import pdb


ALLOWED_EXTENSIONS = ['csv']


class DriverAuth(Auth):

    def get_user_model(self):
        return Driver


class DriverResource(RestResource):
    exclude = ('password')

    def get_query(self):
        return Driver.select().where(Driver.is_admin == False)


auth = DriverAuth(app, db)

public_auth = Authentication(protected_methods=['POST'])
user_auth = UserAuthentication(auth, protected_methods=['GET', 'PUT', 'DELETE'])


# instantiate public api for the data
api = RestAPI(app, default_auth=user_auth)


api.register(Driver, DriverResource)
api.setup()


@app.route('/api/signup/', methods=['POST'])
def register_driver():
    driver = request.get_json()
    try:
        Driver.create(username=driver['username'], password=driver['password'], name=driver['name'], email=driver[
                      'email'], telnumber=driver['telnumber'], address=driver['address'], car=driver['car'])

        return make_response(json.dumps({'result': True}))
    except IntegrityError as e:
        field = e.message.spli('.')[1]
        msg = 'There is already driver with such ' + field + '.'
        return make_response(json.dumps({'error': msg})), 400


@app.route('/api/me/', methods=['GET'])
@auth.login_required
def get_me():
    current_user = auth.get_context_user()['user']
    me = current_user.__dict__['_data']
    me['lastmodified'] = me['lastmodified'].isoformat()
    me.pop('password', None)
    # pdb.set_trace()
    return make_response(json.dumps(me))


@app.route('/api/export/driver/', methods=['GET'])
@auth.login_required
def export_drivers():
    current_user = auth.get_context_user()['user']
    if not current_user.is_admin:
        return 401
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


@app.route('/api/import/driver/', methods=['GET', 'POST'])
@auth.login_required
def import_background_checks():
    current_user = auth.get_context_user()['user']
    if not current_user.is_admin:
        return 401
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

        now = datetime.now()

        Driver.update(status=1, lastmodified=datetime.now()).where(
            Driver.id << clean).execute()
        Driver.update(status=2, lastmodified=datetime.now()).where(
            Driver.id << discrepancy).execute()
        Driver.update(status=3, lastmodified=datetime.now()).where(
            Driver.id << fake).execute()

        cursor = Driver.select(Driver.id, Driver.name, Driver.status).where(
            Driver.lastmodified >= now).dicts().execute().cursor

        drivers = [dict(id=row[0], name=row[1], status=row[2])
                   for row in cursor.fetchall()]
        return make_response(json.dumps(drivers))
    return make_response("nope")
