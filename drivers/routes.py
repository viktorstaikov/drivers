from flask import render_template
from drivers import app


@app.route('/')
def index():
    return render_template('index.html', name='Viktor')
