import unittest
import json
import os

from datetime import datetime

os.environ['DATABASE_URL'] = 'sqlite://'  # set before importing from models to use in memory db

from models import Base, engine, Patient, VitalInfo
from server import app


class TestServer(unittest.TestCase):
    app = None

    def setUp(self):
        self.app = app.test_client()
        Base.metadata.create_all(bind=engine)

    def test_add_patient(self):
        self.app.post('/patients/', data=json.dumps({"firstname": "John", "lastname": "Doe", "nhi": "123ABC"}))
        assert Patient.query.get('123ABC') is not None

    def test_add_vitalinfo(self):
        now = datetime.now()
        self.app.post('/patients/123ABC/vitalinfos/', data=json.dumps({"check_in_time": now.isoformat()}))
        assert VitalInfo.query.get(1).check_in_time == now

    def test_delete_vitalinfo(self):
        self.app.delete('/patients/123ABC/vitalinfos/1/')
        assert len(VitalInfo.query.all()) == 0

if __name__ == '__main__':
    unittest.main()
