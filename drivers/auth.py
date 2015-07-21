from flask_peewee.auth import Auth
from flask import make_response, request
from models import Driver
import json


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
            return make_response(json.dumps({'error': 'Incorrect username or password'})), 400
        # return super(DriverAuth, self).login()

    def get_urls(self):
        return (
            ('/logout/', super(DriverAuth, self).logout),
            ('/login/', self.login),
        )
