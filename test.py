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

    def test_new_patient(self):
        self.app.post('/patients/', data=json.dumps({"firstname": "John", "lastname": "Doe", "nhi": "123ABC"}))
        assert Patient.query.get('123ABC') is not None

    def test_new_vitalinfo(self):
        self.app.delete('/patients/123ABC/vitalinfos/1/')
        now = datetime.now()
        self.app.post('/patients/123ABC/vitalinfos/', data=json.dumps({"check_in_time": now.isoformat()}))
        assert VitalInfo.query.get(1).check_in_time is not None

    def test_update_vitalinfo(self):
        self.app.post('/patients/123ABC/vitalinfos/1/', data=json.dumps({"location": "Been updated"}))
        assert VitalInfo.query.get(1).location == "Been updated"

    def test_delete_vitalinfo(self):
        self.app.delete('/patients/123ABC/vitalinfos/1/')
        assert VitalInfo.query.get(1) is None

    def test_delete_patient(self):
        self.app.delete('/patients/123ABC/')
        assert Patient.query.get('123ABC') is None

if __name__ == '__main__':
    unittest.main()
