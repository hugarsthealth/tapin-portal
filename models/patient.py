from server import db


class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    nhi = db.Column(db.String(10), unique=True, nullable=False)
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

    def to_dict(self):
        temp = self.__dict__.copy()
        del temp['_sa_instance_state']
        temp['vital_info_url'] = "/patients/{}/vitalinfos/".format(self.patient_id)
        temp['dob'] = self.dob.isoformat()
        temp['last_check_in'] = self.last_check_in.isoformat()
        return temp

    def __repr__(self):
        return '<Patient (id: {}, nhi: {}, name: {})>'.format(self.patient_id, self.nhi, self.name)
