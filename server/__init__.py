#!/usr/bin/env python
import os
from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = False if "PRODUCTION" in os.environ else True

import server.vsm
