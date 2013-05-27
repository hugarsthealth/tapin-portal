from datetime import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Date, Float, Boolean

from models import Base


class VitalInfo(Base):
    """
    The VitalInfo class is a database backed model representing a Patient's
    vital information at the time of a check in. It contains data which would
    normally be entered on the form used to check in to a hospital.

    """

    __tablename__ = 'vital_info'
    vital_info_id = Column(Integer, primary_key=True)
    check_in_time = Column(DateTime)
    patient_nhi = Column(String(10), ForeignKey("patient.nhi"))
    firstname = Column(String(250))
    lastname = Column(String(250))
    occupation = Column(String(250))
    citizen_resident = Column(Boolean)
    contact_num = Column(String(20))
    gender = Column(String(250))
    dob = Column(Date)
    weight_value = Column(Float)
    weight_unit = Column(String(50))
    height_value = Column(Float)
    height_unit = Column(String(50))
    blood_type = Column(String(5))
    smoker = Column(Boolean)
    drinker = Column(Boolean)
    family_hist = Column(String(2500))
    overseas_recently = Column(Boolean)
    overseas_dests = Column(String(2500))
    medical_conditions = Column(String(2500))
    allergies = Column(String(2500))
    location = Column(String(50))

    def __init__(self, **kwargs):
        self.deserialize(kwargs)

    def serialize(self):
        return {
            "vital_info_id": self.vital_info_id,
            "check_in_time": self.check_in_time.isoformat() if self.check_in_time else None,
            "patient_nhi": self.patient_nhi,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "occupation": self.occupation,
            "citizen_resident": self.citizen_resident,
            "contact_num": self.contact_num,
            "gender": self.gender,
            "dob": self.dob.isoformat() if self.dob else None,
            "weight_value": self.weight_value,
            "weight_unit": self.weight_unit,
            "height_value": self.height_value,
            "height_unit": self.height_unit,
            "blood_type": self.blood_type,
            "smoker": self.smoker,
            "drinker": self.drinker,
            "family_hist": self.family_hist.split(';') if self.family_hist else None,
            "overseas_recently": self.overseas_recently,
            "overseas_dests": self.overseas_dests.split(';') if self.overseas_dests else None,
            "medical_conditions": self.medical_conditions.split(';') if self.medical_conditions else None,
            "allergies": self.allergies.split(';') if self.allergies else None,
            "location": self.location
        }

    def deserialize(self, data):
        """
        Populate a VitalInfo object with data from a dictionary

        Arguments:
        data -- a dictionary containing data to put on the VitalInfo.

        """
        for key in data:
            if not hasattr(self, key):
                continue

            if key in ['family_hist', 'overseas_dests', 'medical_conditions', 'allergies'] and isinstance(data[key], list):
                # These keys are lists stored as semicolon delimited strings in the db
                setattr(self, key, ';'.join(data[key]))
                continue

            if key in ['check_in_time'] and (isinstance(data[key], unicode) or isinstance(data[key], str)):
                # If check in time is given as a string, parse into a datetime
                setattr(self, key, datetime.strptime(
                    data[key], "%Y-%m-%dT%H:%M:%S.%f"))
                continue

            if key in ['dob'] and (isinstance(data[key], unicode) or isinstance(data[key], str)):
                # If dob is given as a string, parse into a date
                setattr(self, key, datetime.strptime(
                    data[key], "%Y-%m-%d").date())
                continue

            setattr(self, key, data[key])

    def __repr__(self):
        return '<VitalInfo (id: {}, patient: {}, time: {})>'.format(self.vital_info_id, self.patient_nhi, self.check_in_time)
