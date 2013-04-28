from server import app

import json


class Patient(app.db.Model):
    patient_id = app.db.Column(app.db.Integer, primary_key=True)
    firstname = app.db.Column(app.db.String(250), nullable=False)
    lastname = app.db.Column(app.db.String(250), nullable=False)
    nhi = app.db.Column(app.db.String(10), unique=True, nullable=False)
    occupation = app.db.Column(app.db.String(250))
    citizen_resident = app.db.Column(app.db.Boolean)
    contact_num = app.db.Column(app.db.String(20))
    gender = app.db.Column(app.db.String(250))
    dob = app.db.Column(app.db.Date)
    last_check_in = app.db.Column(app.db.Date)

    """docstring for Patient"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return json.dumps(self.__dict__, indent=2)
