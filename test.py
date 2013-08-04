import unittest
import json
import os

from datetime import datetime

# set before importing from models to use in memory db
os.environ['DATABASE_URL'] = 'sqlite://'

from models import db, Base, engine, Patient, CheckIn, Department
from server import app


class VsmTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()

    def setUp(self):
        self.now = datetime.now().isoformat()

        Base.metadata.bind = engine
        Base.metadata.drop_all()
        Base.metadata.create_all()


class TestPatient(VsmTest):

    def test_new_patient(self):
        self.app.post('/patients', data=json.dumps({"nhi": "123ABC"}))
        assert Patient.query.get('123ABC') is not None

    def test_new_patient_idempotent(self):
        self.app.post('/patients', data=json.dumps({"nhi": "123ABC"}))
        self.app.post('/patients', data=json.dumps({"nhi": "123ABC"}))
        assert Patient.query.get('123ABC') is not None

    def test_new_patient_with_checkin(self):
        self.app.post('/patients',
                      data=json.dumps({"nhi": "111AAA", "checkin": {"checkin_time": self.now}}))

        assert Patient.query.get('111AAA').checkins

    def test_delete_patient(self):
        self.app.delete('/patients/123ABC')
        assert Patient.query.get('123ABC') is None


class TestCheckIn(VsmTest):

    def setUp(self):
        super(TestCheckIn, self).setUp()

        db.add(Patient(nhi="123ABC"))
        db.add(CheckIn(patient_nhi="123ABC", checkin_time=self.now))

        db.commit()

    def test_new_checkin(self):
        self.app.post('/patients/123ABC/checkins',
                      data=json.dumps({"checkin_time": self.now}))

        assert len(Patient.query.get('123ABC').checkins) == 2

    def test_update_checkin(self):
        self.app.post('/patients/123ABC/checkins/1',
                      data=json.dumps({"location": "Been updated"}))

        assert CheckIn.query.get(1).location == "Been updated"

    def test_delete_checkin(self):
        self.app.delete('/patients/123ABC/checkins/1')
        assert CheckIn.query.get(1) is None

    def test_latest_checkin(self):
        self.app.post('/patients/123ABC/checkins',
                      data=json.dumps({"checkin_time": self.now}))

        assert Patient.query.get(
            '123ABC').latest_checkin_time.isoformat() == self.now


class TestDepartment(VsmTest):

    def setUp(self):
        super(TestDepartment, self).setUp()

        cardiology = Department(department_name="Cardiology")
        oncology = Department(department_name="Oncology")

        p1 = Patient(nhi="A")
        p2 = Patient(nhi="B")
        p3 = Patient(nhi="C")

        p1.departments.append(cardiology)
        p2.departments.append(oncology)
        p3.departments.append(cardiology)
        p3.departments.append(oncology)

        map(db.add, (p1, p2, p3))
        db.commit()

        self.app.post('/login', data={"department": "Cardiology"})

    def test_departments_get(self):
        rv = self.app.get('/departments')
        departments = json.loads(rv.data)

        assert len(departments) == 2

    def test_department_patients_get(self):
        rv = self.app.get('/patients')
        patients = json.loads(rv.data)

        assert all(any(d['department_name'] == 'Cardiology' for d in p['departments']) for p in patients)

    def test_department_patient_get(self):
        rv = self.app.get('/patients/B')
        assert rv.data == "No patient with NHI B"


if __name__ == '__main__':
    unittest.main()
