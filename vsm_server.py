#!/usr/bin/env python

import os
import urlparse
import psycopg2

from flask import Flask


app = Flask(__name__)

urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.getenv('DATABASE_URL'))

conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
cur = conn.cursor()


@app.route('/')
def hello():
    return url


@app.route('/patients')
def patients():
    pass


@app.route('/patients/<int:patient_id>', methods=['GET', 'POST'])
def patient(patient_id):
    pass


@app.route('/patients/<int:patient_id>/vitalinfo')
def vital_info():
    pass


@app.route('/patients/<int:patient_id>/vitalinfo/<int:vitalinfo_id>', methods=['GET', 'POST'])
def vital_info_from_id(id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
