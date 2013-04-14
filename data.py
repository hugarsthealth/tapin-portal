import os
import urlparse
import psycopg2


urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.getenv('DATABASE_URL'))

conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
cur = conn.cursor()


def get_patients():
    return {"hi": 1}


def get_patient(patient_id):
    return {"hi": 1}


def get_vital_infos():
    return {"hi": 1}


def get_vital_info(vitalinfo_id):
    return {"hi": 1}
