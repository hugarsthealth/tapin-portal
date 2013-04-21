#!/usr/bin/env python

from random import choice, randrange, getrandbits
import json
import string


def rand_date():
    day = str(randrange(1, 29))
    month = str(randrange(1, 12))
    year = str(randrange(1800, 2012))
    return '/'.join([year, month, day])


def rand_lower_str(length):
    return ''.join(choice(string.lowercase) for i in range(length))


def rand_name(length):
    return rand_lower_str(length).capitalize()


def rand_digit_str(length):
    return ''.join(choice(string.digits) for i in range(length))


def rand_nhi():
    letters = ''.join(choice(string.uppercase) for i in range(3))
    digits = ''.join(choice(string.digits) for i in range(3))
    return letters + digits


def rand_bool():
    return bool(getrandbits(1))


def write_to_file(filename, data):
    f = open(filename, 'w')
    f.writelines(data)
    f.close


def list_of_rand_str(list_length, str_length):
    return [rand_lower_str(str_length) for x in xrange(list_length)]


def generate_patient(patient_id):
    firstname = rand_name(6)
    lastname = rand_name(8)
    nhi = rand_nhi()
    occupation = rand_name(12)
    citizen_resident = rand_bool()
    contact_num = rand_digit_str(10)
    gender = choice(['Male', 'Female'])
    dob = rand_date()
    vital_info_url = "/patients/%s/vitalinfo" % patient_id
    vital_info_ids = []

    return {
        'patient_id': patient_id,
        'firstname': firstname,
        'lastname': lastname,
        'nhi': nhi,
        'occupation': occupation,
        'citizen_resident': citizen_resident,
        'contact_num': contact_num,
        'gender': gender,
        'dob': dob,
        'vital_info_url': vital_info_url,
        'vital_info_ids': vital_info_ids
    }


def generate_vital_info(patient_id, vital_info_id):
    weight_value = randrange(0, 200)
    weight_unit = choice(['kg', 'lb'])
    height_value = randrange(0, 200)
    height_unit = choice(['cm'])
    blood_type = choice(['A', 'B', 'AB', 'O'])
    smoker = rand_bool()
    drinker = rand_bool()
    family_hist = list_of_rand_str(6, 30)
    overseas_recently = rand_bool()
    overseas_destinations = list_of_rand_str(10, 12)
    medical_conditions = list_of_rand_str(6, 20)
    allergies = list_of_rand_str(4, 10)

    return {
        'vital_info_id': vital_info_id,
        'patient_id': patient_id,
        'weight': {'value': weight_value, 'unit': weight_unit},
        'height': {'value': height_value, 'unit': height_unit},
        'blood_type': blood_type,
        'smoker': smoker,
        'drinker': drinker,
        'family_hist': family_hist,
        'overseas': {'recently': overseas_recently, 'destinations': overseas_destinations},
        'medical_conditions': medical_conditions,
        'allergies': allergies
    }


def main():
    NUM_PATIENTS = 10
    MIN_VITAL_INFOS = 1
    MAX_VITAL_INFOS = 20

    vitalinfos = []
    patients = []

    for i in xrange(NUM_PATIENTS):
        patient = generate_patient(i)
        patients.append(patient)

        for j in xrange(randrange(MIN_VITAL_INFOS, MAX_VITAL_INFOS)):
            vitalinfo = generate_vital_info(i, j)
            vitalinfos.append(vitalinfo)

            patient['vital_info_ids'].append(vitalinfo['vital_info_id'])

    with open('patients.json', 'w') as f:
        f.write(json.dumps({'patients': patients}, indent=4))

    with open('vitalinfos.json', 'w') as f:
        f.write(json.dumps({'vitalinfos': vitalinfos}, indent=4))

if __name__ == '__main__':
    main()
