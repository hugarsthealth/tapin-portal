from server import db


class Patient(db.Model):
    nhi = db.Column(db.String(10), primary_key=True)
    firstname = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    occupation = db.Column(db.String(250))
    citizen_resident = db.Column(db.Boolean)
    contact_num = db.Column(db.String(20))
    gender = db.Column(db.String(250))
    dob = db.Column(db.Date)
    last_check_in = db.Column(db.DateTime)
    vitalinfos = db.relationship("VitalInfo", backref="patient", cascade="delete")

    """docstring for Patient"""
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @property
    def name(self):
        return '{0} {1}'.format(self.firstname, self.lastname)

    def serialize(self):
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "nhi": self.nhi,
            "occupation": self.occupation,
            "citizen_resident": self.citizen_resident,
            "contact_num": self.contact_num,
            "gender": self.gender,
            "dob": self.dob.isoformat(),
            "last_check_in": self.last_check_in.isoformat()
        }

    def __repr__(self):
        return '<Patient (nhi: {}, name: {})>'.format(self.nhi, self.name)
