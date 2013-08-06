from datetime import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, DateTime

from models import Base


class Appointment(Base):
    """
    The Appointment class is a database backed model representing a Patient's
    vital information at the time of a check in. It contains data which would
    normally be entered on the form used to check in to a hospital.

    """

    __tablename__ = 'appointment'
    appointment_id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    patient_nhi = Column(String(10), ForeignKey("patient.nhi"))
    reason = Column(String(250))
    location = Column(String(50))

    def __init__(self, **kwargs):
        self.deserialize(kwargs)

    def serialize(self):
        return {
            "appointment_id": self.appointment_id,
            "time": self.time.isoformat() if self.time else None,
            "patient_nhi": self.patient_nhi,
            "reason": self.reason,
            "location": self.location
        }

    def deserialize(self, data):
        """
        Populate a Appointment object with data from a dictionary

        Arguments:
        data -- a dictionary containing data to put on the Appointment.

        """
        for key in data:
            if not hasattr(self, key):
                continue

            if key in ['time'] and (isinstance(data[key], unicode) or isinstance(data[key], str)):
                # If check in time is given as a string, parse into a datetime
                setattr(self, key, datetime.strptime(
                    data[key], "%Y-%m-%dT%H:%M:%S.%f"))
                continue

            setattr(self, key, data[key])

    def __repr__(self):
        return '<Appointment (id: {}, patient: {}, time: {})>'.format(self.appointment_id, self.patient_nhi, self.time)
