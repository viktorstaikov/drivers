from flask import request, session, g, redirect, url_for, abort, render_template
from drivers import app


@app.route('/api/drivers')
def show_entries():
    cur = g.db.execute('select id, name from drivers order by id desc')
    drivers = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
    return json.dumps(drivers)
    # return json.dumps([{'id': 1, 'name': 'John Doe'}])


@app.route('/api/drivers/add', methods=['POST'])
def add_entry():
    # if not session.get('logged_in'):
    #     abort(401)
    g.db.execute('insert into drivers (name) values (?)',
                 [request.form['name']])
    g.db.commit()
    return json.dumps({'result': True})


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            # return redirect(url_for('show_entries'))
            return json.dumps({'result': True})
    # return render_template('login.html', error=error)
    return json.dumps(error), 401


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    # return redirect(url_for('show_entries'))
    return json.dumps({'result': True})
