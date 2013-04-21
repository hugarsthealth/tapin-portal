import json
# import os
# import urlparse
# import psycopg2


# urlparse.uses_netloc.append('postgres')
# url = urlparse.urlparse(os.getenv('DATABASE_URL'))

# conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
# cur = conn.cursor()


def get_patients():
    with open("data/patients.json") as f:
        return json.loads(f.read())


def get_patient(patient_id):
    with open("data/patients.json") as f:
        patients = json.loads(f.read()).get('patients', [])

        for patient in patients:
            if patient.get('patient_id') == patient_id:
                return {"patient": patient}

        return {"Error 404": "Patient not found"}


def store_patient(patient_data):
    pass


def delete_patient(patient_id):
    pass


def update_patient(patient_id, patient_data):
    pass


def get_vital_infos(patient_id):
    with open("data/vitalinfos.json") as f:
        vitalinfos = json.loads(f.read()).get('vitalinfos', [])

        return {"vitalinfos": [vi for vi in vitalinfos if vi.get('patient_id') == patient_id]}


def get_vital_info(patient_id, vital_info_id):
    with open("data/vitalinfos.json") as f:
        vitalinfos = json.loads(f.read()).get('vitalinfos', [])

        for vitalinfo in vitalinfos:
            if vitalinfo.get('vital_info_id') == vital_info_id and vitalinfo.get('patient_id') == patient_id:
                return {"vitalinfo": vitalinfo}

        return {"Error 404": "Vital info not found"}


def store_vital_info(patient_id, vital_info_data):
    pass


def delete_vital_info(vital_info_id):
    pass


def update_vital_info(vital_info_id, vital_info_data):
    pass
