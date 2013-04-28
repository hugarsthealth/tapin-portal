from server import app


class VitalInfo(app.db.Model):
    vital_info_id = app.db.Column(app.db.Integer, primary_key=True)
    check_in_time = app.db.Column(app.db.DateTime, nullable=False)
    patient_id = app.db.Column(app.db.Integer, app.db.ForeignKey("patient.patient_id"), nullable=False)
    weight_value = app.db.Column(app.db.Float)
    weight_unit = app.db.Column(app.db.String(50))
    height_value = app.db.Column(app.db.Float)
    height_unit = app.db.Column(app.db.String(50))
    blood_type = app.db.Column(app.db.String(5))
    smoker = app.db.Column(app.db.Boolean)
    drinker = app.db.Column(app.db.Boolean)
    family_hist = app.db.Column(app.db.String(2500))
    overseas_recently = app.db.Column(app.db.Boolean)
    overseas_dests = app.db.Column(app.db.String(2500))
    medical_conditions = app.db.Column(app.db.String(2500))
    allergies = app.db.Column(app.db.String(2500))

    """docstring for VitalInfo"""
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def to_dict(self):
        temp = self.__dict__.copy()
        del temp['_sa_instance_state']
        temp['check_in_time'] = temp['check_in_time'].isoformat()
        return temp

    def __repr__(self):
        return '<VitalInfo (id: {}, patient: {})>'.format(self.vital_info_id, self.patient_id)
