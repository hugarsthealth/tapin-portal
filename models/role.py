from sqlalchemy import Column, String, Integer

from models import Base


class Role(Base):
    __tablename__ = 'role'
    role_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    """docstring for Patient"""
    def __init__(self, **kwargs):
        self.deserialize(kwargs)

    def serialize(self):
        return {
            "role_id": self.role_id,
            "name": self.name
        }

    def deserialize(self, data):
        for key in data:
            if not data[key] or not hasattr(self, key):
                continue

            setattr(self, key, data[key])

    def __repr__(self):
        return '<Role (name: {})>'.format(self.name)
