from datetime import datetime

from sqlalchemy import Column, String, Boolean, Date, DateTime
from sqlalchemy.orm import relationship

from models import Base


class Patient(Base):
    __tablename__ = 'patient'
    nhi = Column(String(10), primary_key=True)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    occupation = Column(String(250))
    citizen_resident = Column(Boolean)
    contact_num = Column(String(20))
    gender = Column(String(250))
    dob = Column(Date)
    last_check_in = Column(DateTime)
    vitalinfos = relationship("VitalInfo", backref="patient", cascade="delete")

    """docstring for Patient"""
    def __init__(self, **kwargs):
        self.deserialize(kwargs)

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

    def deserialize(self, data):
        for key in data:
            if key in ['last_check_in']:
                setattr(self, key, datetime.strptime(data[key], "%Y-%m-%dT%H:%M:%S.%f"))
                continue

            if key in ['dob']:
                setattr(self, key, datetime.strptime(data[key], "%Y-%m-%d"))

            setattr(self, key, data[key])

    def __repr__(self):
        return '<Patient (nhi: {}, name: {})>'.format(self.nhi, self.name)
