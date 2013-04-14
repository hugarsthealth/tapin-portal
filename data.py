import os
import json
import urlparse
import psycopg2


# urlparse.uses_netloc.append('postgres')
# url = urlparse.urlparse(os.getenv('DATABASE_URL'))

# conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
# cur = conn.cursor()


def get_patients():
    with open("sampledata/patients.json") as f:
        return json.loads(f.read())


def get_patient(patient_id):
    with open("sampledata/patients.json") as f:
        patients = json.loads(f.read())

        for patient in patients.get('patients'):
            if patient.get('patient_id') == patient_id:
                return patient


def get_vital_infos(patient_id):
    with open("sampledata/vitalinfos.json") as f:
        vitalinfos = json.loads(f.read())
        return {"vitalinfo": [vi for vi in vitalinfos.get('vitalinfo') if vi.get('patient_id') == patient_id]}


def get_vital_info(vitalinfo_id):
    with open("sampledata/vitalinfos.json") as f:
        vitalinfos = json.loads(f.read())

        for vitalinfo in vitalinfos.get('vitalinfo'):
            if vitalinfo.get('vitalinfo_id') == vitalinfo_id:
                return vitalinfo
