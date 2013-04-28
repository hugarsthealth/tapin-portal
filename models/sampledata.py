#!/usr/bin/env python

from random import choice, randrange, getrandbits, randint
from datetime import datetime, timedelta
from server import app
from models.patient import Patient
from models.vitalinfo import VitalInfo
import json
import string

with open('models/dictionary.txt') as f:
    words = [word.strip() for word in f.read().split('\n')]


def rand_date(from_days_ago=2000):
    return datetime.now() - timedelta(randint(0, from_days_ago))


def rand_word():
    return choice(words).lower()


def rand_sentence(length):
    return ' '.join([choice(words) for x in xrange(length)]).capitalize()


def rand_name():
    return rand_word().capitalize()


def rand_digit_str(length):
    return ''.join(choice(string.digits) for i in range(length))


def rand_nhi():
    letters = ''.join(choice(string.uppercase) for i in range(3))
    digits = ''.join(choice(string.digits) for i in range(3))
    return letters + digits


def rand_bool():
    return bool(getrandbits(1))


def list_of_rand_sentences(list_length, sentence_length):
    return ';'.join([rand_sentence(sentence_length) for x in xrange(list_length)])


def generate_patient(patient_id):
    firstname = rand_name()
    lastname = rand_name()
    nhi = rand_nhi()
    occupation = rand_name()
    citizen_resident = rand_bool()
    contact_num = rand_digit_str(10)
    gender = choice(['Male', 'Female'])
    dob = rand_date(30000)
    last_check_in = None

    return {
        #'patient_id': patient_id,
        'firstname': firstname,
        'lastname': lastname,
        'nhi': nhi,
        'occupation': occupation,
        'citizen_resident': citizen_resident,
        'contact_num': contact_num,
        'gender': gender,
        'dob': dob,
        'last_check_in': last_check_in,
    }


def generate_vital_info(patient_id, vital_info_id):
    check_in_time = rand_date()
    weight_value = randrange(0, 200)
    weight_unit = choice(['kg', 'lb'])
    height_value = randrange(0, 200)
    height_unit = choice(['cm'])
    blood_type = choice(['A', 'B', 'AB', 'O'])
    smoker = rand_bool()
    drinker = rand_bool()
    family_hist = list_of_rand_sentences(6, 30)
    overseas_recently = rand_bool()
    overseas_dests = list_of_rand_sentences(10, 12)
    medical_conditions = list_of_rand_sentences(6, 20)
    allergies = list_of_rand_sentences(4, 10)

    return {
        'vital_info_id': vital_info_id,
        'check_in_time': check_in_time,
        'patient_id': patient_id,
        'weight_value': weight_value,
        'weight_unit': weight_unit,
        'height_value': height_value,
        'height_unit': height_unit,
        'blood_type': blood_type,
        'smoker': smoker,
        'drinker': drinker,
        'family_hist': family_hist,
        'overseas_recently': overseas_recently,
        'overseas_dests': overseas_dests,
        'medical_conditions': medical_conditions,
        'allergies': allergies
    }


def generate_sample_data():
    NUM_PATIENTS = 2
    MIN_VITAL_INFOS = 1
    MAX_VITAL_INFOS = 2

    patients = []
    vitalinfos = []

    for i in xrange(NUM_PATIENTS):
        patient = generate_patient(i)
        app.db.session.add(Patient(**patient))

        for j in xrange(randrange(MIN_VITAL_INFOS, MAX_VITAL_INFOS)):
            vitalinfo = generate_vital_info(i, j)
            app.db.session.add(VitalInfo(**vitalinfo))

            lci = patient['last_check_in']
            vid = vitalinfo['check_in_time']

            lci = vid if lci is None or vid > lci else lci
            patient['last_check_in'] = lci

    app.db.session.commit()

    return (patients, vitalinfos)

def main():
    patients, vitalinfos = generate_sample_data()

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None

#    with open('patients.json', 'w') as f:
#        f.write(json.dumps({'patients': patients}, indent=2, default=dthandler))
#
#    with open('vitalinfos.json', 'w') as f:
#        f.write(json.dumps({'vitalinfos': vitalinfos}, indent=2, default=dthandler))

if __name__ == '__main__':
    main()
