#!/usr/bin/env python

import os
import psycopg2

from flask import Flask


app = Flask(__name__)
dburl = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(dburl)


@app.route('/')
def hello():
    return dburl + conn


@app.route('/patients')
def patients():
    pass


@app.route('/patients/<int:id>', methods=['GET', 'POST'])
def patient(id):
    pass


@app.route('/patients/<int:id>/vitalinfo')
def vital_info():
    pass


@app.route('/patients/<int:id>/vitalinfo/<int:id>', methods=['GET', 'POST'])
def vital_info_from_id(id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
