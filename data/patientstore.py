import sqlite3
import sampledata


class SQLitePatientStore(object):

    """docstring for SQLitePatientStore"""
    def __init__(self, dbname):
        super(SQLitePatientStore, self).__init__()
        self.dbname = dbname
        self.conn = None
        self._connect()

        if not self._tables_exist():
            print("CREATING DATABASE")
            self._create_tables()
            self._populate_tables(*sampledata.generate_sample_data())
            print("DATABASE CREATED")

    def _connect(self):
        if self.conn:
            self.conn.close()

        self.conn = sqlite3.connect(self.dbname)
        self.conn.row_factory = sqlite3.Row

    def _tables_exist(self):
        return self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patients'").fetchone() is not None

    def _populate_tables(self, patients, vitalinfos):
        for p in patients:
            self.store_patient(p)
        for v in vitalinfos:
            self.store_vital_info(v['patient_id'], v)

    def _create_tables(self):
        with open('schema.sql') as f:
            self.conn.executescript(f.read())
            self.conn.commit()

    def _patient_row_to_obj(self, row):
        return {
            "firstname": row["firstname"],
            "lastname": row["lastname"],
            "nhi": row["nhi"],
            "vital_info_url": "/patients/{}/vitalinfos/".format(row["patient_id"]),
            "occupation": row["occupation"],
            "citizen_resident": bool(row["citizen_resident"]),
            "contact_num": row["contact_num"],
            "gender": row["gender"],
            "patient_id": row["patient_id"],
            "dob": row["dob"],
            "last_check_in": None,
            "vital_info_ids": []
        }

    def _patient_vital_ids(self, patient_id):
        return [r[0] for r in self.conn.execute("SELECT vital_info_id FROM vitalinfos WHERE patient_id=?", (patient_id,))]

    def get_patients(self):
        patients = [self._patient_row_to_obj(r) for r in self.conn.execute("SELECT * FROM patients")]

        for p in patients:
            p['vital_info_ids'] = self._patient_vital_ids(p['patient_id'])

        return {"patients": patients}

    def get_patient(self, patient_id):
        pass

    def store_patient(self, patient_data):
        self.conn.execute("INSERT INTO patients VALUES (?,?,?,?,?,?,?,?,?)",
                         (None, patient_data['firstname'], patient_data['lastname'], patient_data['nhi'],
                          patient_data['occupation'], patient_data['citizen_resident'],
                          patient_data['contact_num'], patient_data['gender'], patient_data['dob']))
        self.conn.commit()

    def delete_patient(self, patient_id):
        pass

    def update_patient(self, patient_id, patient_data):
        pass

    def get_vital_infos(self, patient_id):
        pass

    def get_vital_info(self, patient_id, vital_info_id):
        pass

    def store_vital_info(self, patient_id, vital_info_data):
        self.conn.execute("INSERT INTO vitalinfos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (None,
                          patient_id,
                          vital_info_data['weight']['value'],
                          vital_info_data['weight']['unit'],
                          vital_info_data['height']['value'],
                          vital_info_data['height']['unit'],
                          vital_info_data['check_in_time'],
                          vital_info_data['drinker'],
                          vital_info_data['smoker'],
                          vital_info_data['blood_type'],
                          vital_info_data['overseas']['recently'],
                          ';'.join(vital_info_data['overseas']['destinations']),
                          ';'.join(vital_info_data['medical_conditions']),
                          ';'.join(vital_info_data['allergies']),
                          ';'.join(vital_info_data['family_hist'])))
        self.conn.commit()

    def delete_vital_info(self, vital_info_id):
        pass

    def update_vital_info(self, vital_info_id, vital_info_data):
        pass


class PostgresPatientStore(object):

    """docstring for PostgresPatientStore"""
    def __init__(self):
        super(PostgresPatientStore, self).__init__()

    def get_patients(self):
        pass

    def get_patient(self, patient_id):
        pass

    def store_patient(self, patient_data):
        pass

    def delete_patient(self, patient_id):
        pass

    def update_patient(self, patient_id, patient_data):
        pass

    def get_vital_infos(self, patient_id):
        pass

    def get_vital_info(self, patient_id, vital_info_id):
        pass

    def store_vital_info(self, patient_id, vital_info_data):
        pass

    def delete_vital_info(self, vital_info_id):
        pass

    def update_vital_info(self, vital_info_id, vital_info_data):
        pass
