#!/usr/bin/env python
import os

from flask import Flask

from models import db

app = Flask(__name__)

app.config.update(
    DEBUG=False if "PRODUCTION" in os.environ else True,
    SECRET_KEY='g\x7f\xc4\xeb\x84\xb38\xe3\x8f\x8e\x14Tu\x18h\x96\xcbp#\xbc\xa0\xa3\xcd\xdc'
)


@app.teardown_request
def shutdown_session(exception=None):
    db.remove()

import server.vsm
