#!/usr/bin/env python
import os
import urlparse
import psycopg2

from data.patientstore import PostgresPatientStore, SQLitePatientStore
from flask import Flask
app = Flask(__name__)

app.config['DEBUG'] = False if "PRODUCTION" in os.environ else True

if "DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.getenv('DATABASE_URL'))

    conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
    app.db = PostgresPatientStore(conn)
else:
    @app.before_request
    def before_request():
        app.db = SQLitePatientStore('patients.db')

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(app, 'db'):
            app.db.conn.close()


import server.vsm
