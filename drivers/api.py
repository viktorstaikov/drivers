from flask_peewee.rest import RestAPI, Authentication, UserAuthentication, RestResource
from flask_peewee.auth import Auth
from flask import make_response, request
from peewee import IntegrityError
from models import Driver
from drivers import app, db
from datetime import datetime
import json

import pdb


class DriverAuth(Auth):

    def get_user_model(self):
        return Driver

    def login(self):
        print('custom auth login')
        user = request.get_json()
        username = str(user['username'])
        password = str(user['password'])
        # pdb.set_trace()
        authenticated_user = self.authenticate(username, password)
        if authenticated_user:
            self.login_user(authenticated_user)
            me = self.get_logged_in_user()
            return make_response(me.to_JSON())
        else:
            return make_response(json.dumps({'error': 'Incorrect username or password'}))
        # return super(DriverAuth, self).login()

    def get_urls(self):
        return (
            ('/logout/', super(DriverAuth, self).logout),
            ('/login/', self.login),
        )


class DriverResource(RestResource):
    exclude = ('password')

    def get_query(self):
        return Driver.select().where(Driver.is_admin == False)


ALLOWED_EXTENSIONS = ['csv']

auth = DriverAuth(app, db)

public_auth = Authentication(protected_methods=['POST'])
user_auth = UserAuthentication(auth, protected_methods=['GET', 'PUT', 'DELETE'])

# instantiate public api for the data
api = RestAPI(app, default_auth=user_auth)
api.register(Driver, DriverResource)
api.setup()


def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_current_user():
    return auth.get_context_user()['user']


def is_current_user_admin():
    return auth.get_context_user()['user'].is_admin


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
    current_user = get_current_user()
    me = current_user.to_JSON()
    return make_response(me)


@app.route('/api/export/driver/', methods=['GET'])
@auth.login_required
def export_drivers():
    if not is_current_user_admin():
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


@app.route('/api/import/driver/', methods=['GET', 'POST'])
@auth.login_required
def import_background_checks():
    if not is_current_user_admin():
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
