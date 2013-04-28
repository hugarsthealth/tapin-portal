from server import app


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
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @property
    def name(self):
        return '{0} {1}'.format(self.firstname, self.lastname)

    def to_dict(self):
        temp = self.__dict__.copy()
        del temp['_sa_instance_state']
        temp['vital_info_url'] = "/patients/{}/vitalinfos/".format(self.patient_id)
        return temp

    def __repr__(self):
        return '<Patient (nhi: {}, name: {})>'.format(self.nhi, self.name)
