#!/usr/bin/env python

from random import choice, randrange, getrandbits
import json
import string

def rand_lower_str(length):
    return ''.join(choice(string.lowercase) for i in range(length))

def rand_name(length):
    return rand_lower_str(length).capitalize()

def rand_digit_str(length):
    return ''.join(choice(string.digits) for i in range(length))

def rand_nhi():
    letters = ''.join(choice(string.uppercase) for i in range(3))
    digits =  ''.join(choice(string.digits) for i in range(3))
    return letters + digits

def rand_bool():
    return bool(getrandbits(1))

def write_to_file(filename, data):
    f = open(filename, 'w')
    f.writelines(data)
    f.close

def list_of_rand_str(list_length, str_length):
    lines = []
    for line in range(list_length):
        lines.append(rand_lower_str(str_length))
    return lines

patient_id = randrange(0, 100000)
firstname = rand_name(6)
lastname = rand_name(8)
nhi = rand_nhi()
occupation = rand_name(12)
citizen_resident = rand_bool()
contact_num = rand_digit_str(10)
gender = choice(['Male', 'Female'])
dob = rand_lower_str(4) #TODO

vital_info_id = randrange(0, 10000000)
vital_info_url = "/patients/%s/vitalinfo" % patient_id
weight_value = randrange(0, 200)
weight_unit = choice(['kg', 'lb'])
height_value = randrange(0, 200)
height_unit = choice(['cm'])
blood_type = choice(['A', 'B', 'AB', 'O'])
smoker = rand_bool()
drinker = rand_bool()
family_hist = list_of_rand_str(6, 30)
overseas_recently = rand_lower_str(20)
overseas_destinations = list_of_rand_str(10, 12)
medical_conditions = list_of_rand_str(6, 20)
allergies = list_of_rand_str(4, 10)

patient = {
    'patient_id': patient_id,
    'firstname': firstname,
    'lastname': lastname,
    'nhi': nhi,
    'occupation': occupation,
    'citizen_resident': citizen_resident,
    'contact_num': contact_num,
    'gender': gender,
    'dob': dob,
}

vital_info = {
    'vital_info_id': vital_info_id,
    'vital_info_url': vital_info_url,
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

patient_data = json.dumps(patient, sort_keys=True, indent=4)
vital_info_data = json.dumps(vital_info, sort_keys=True, indent=4)

write_to_file('patient.json', patient_data)
write_to_file('vital_info.json', vital_info_data)
