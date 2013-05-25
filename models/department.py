from sqlalchemy import Column, String, Integer

from models import Base


class Department(Base):
    __tablename__ = 'department'
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String, unique=True, nullable=False)

    """docstring for Patient"""
    def __init__(self, **kwargs):
        self.deserialize(kwargs)

    def serialize(self):
        return {
            "department_id": self.department_id,
            "department_name": self.department_name
        }

    def deserialize(self, data):
        for key in data:
            if not hasattr(self, key):
                continue

            setattr(self, key, data[key])

    def __repr__(self):
        return '<Department (id: {}, name: {})>'.format(self.department_id, self.department_name)
