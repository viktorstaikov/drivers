from flask import request, session, g, redirect, url_for, abort, render_template
from drivers import app

import json


@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    cur = g.db.execute('select * from drivers order by id desc')
    drivers = [dict(id=row[0], name=row[1], email=row[2], status=row[3])
               for row in cur.fetchall()]
    return json.dumps(drivers)
    # return json.dumps([{'id': 1, 'name': 'John Doe'}])


@app.route('/api/drivers/<id>', methods=['GET'])
def get_driver(id):
    cur = g.db.execute(
        'select * from drivers where id == ' + id + ' order by id desc')
    drivers = [dict(id=row[0], name=row[1], email=row[2], status=row[3])
               for row in cur.fetchall()]
    return json.dumps(drivers[0])


@app.route('/api/drivers', methods=['POST'])
def add_driver():
    # if not session.get('logged_in'):
    #     abort(401)
    driver = request.get_json()
    g.db.execute('insert into drivers (name, email, status) values (?, ?, 0)',
                 [driver['name'], driver['email']])
    g.db.commit()
    return json.dumps({'result': True})


@app.route('/api/drivers/<id>', methods=['PUT'])
def update_driver():
    return json.dumps({'result': False}), 400


@app.route('/api/drivers/<id>', methods=['DELETE'])
def delete_driver():
    g.db.execute('delete from drivers where id == ' + id)
    g.db.commit()
    return json.dumps({'result': True})
