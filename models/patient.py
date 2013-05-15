from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from models import Base, patient_role_table


class Patient(Base):
    __tablename__ = 'patient'
    nhi = Column(String(10), primary_key=True)
    latest_check_in = Column(DateTime)

    roles = relationship(
        "Role",
        secondary=patient_role_table,
        backref="patients"
    )

    vitalinfos = relationship(
        "VitalInfo",
        backref="patient",
        cascade="delete",
        order_by="desc(VitalInfo.check_in_time)"
    )

    """docstring for Patient"""
    def __init__(self, **kwargs):
        self.deserialize(kwargs)

    @property
    def name(self):
        return '{0} {1}'.format(self.firstname, self.lastname)

    def serialize(self):
        return {
            "nhi": self.nhi,
            "roles": [r.serialize() for r in self.roles],
            "latest_check_in": self.latest_check_in.isoformat() if self.latest_check_in else None,
            "latest_vitalinfo": self.vitalinfos[0].serialize() if self.vitalinfos else None
        }

    def deserialize(self, data):
        for key in data:
            if not data[key] or not hasattr(self, key):
                continue

            setattr(self, key, data[key])

    def __repr__(self):
        return '<Patient (nhi: {})>'.format(self.nhi)
