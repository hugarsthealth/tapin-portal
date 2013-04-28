#!/usr/bin/env python
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['DEBUG'] = False if "PRODUCTION" in os.environ else True

if "DATABASE_URL" in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

app.db = SQLAlchemy(app)

if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
    app.db.create_all()

import server.vsm