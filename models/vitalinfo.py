from server import db


class VitalInfo(db.Model):
    vital_info_id = db.Column(db.Integer, primary_key=True)
    check_in_time = db.Column(db.DateTime, nullable=False)
    patient_nhi = db.Column(db.String(10), db.ForeignKey("patient.nhi"), nullable=False)
    weight_value = db.Column(db.Float)
    weight_unit = db.Column(db.String(50))
    height_value = db.Column(db.Float)
    height_unit = db.Column(db.String(50))
    blood_type = db.Column(db.String(5))
    smoker = db.Column(db.Boolean)
    drinker = db.Column(db.Boolean)
    family_hist = db.Column(db.String(2500))
    overseas_recently = db.Column(db.Boolean)
    overseas_dests = db.Column(db.String(2500))
    medical_conditions = db.Column(db.String(2500))
    allergies = db.Column(db.String(2500))

    """docstring for VitalInfo"""
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def serialize(self):
        return {
            "vital_info_id": self.vital_info_id,
            "check_in_time": self.check_in_time.isoformat(),
            "patient_nhi": self.patient_nhi,
            "weight_value": self.weight_value,
            "weight_unit": self.weight_unit,
            "height_value": self.height_value,
            "height_unit": self.height_unit,
            "blood_type": self.blood_type,
            "smoker": self.smoker,
            "drinker": self.drinker,
            "family_hist": self.family_hist.split(';'),
            "overseas_recently": self.overseas_recently,
            "overseas_dests": self.overseas_dests.split(';'),
            "medical_conditions": self.medical_conditions.split(';'),
            "allergies": self.allergies.split(';')
        }

    def __repr__(self):
        return '<VitalInfo (id: {}, patient: {})>'.format(self.vital_info_id, self.patient_nhi)
