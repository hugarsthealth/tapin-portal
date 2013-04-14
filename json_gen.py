#!/usr/bin/env python

import json
from random import choice, randrange
import string

def rand_lower_str(length):
    return ''.join(choice(string.lowercase) for i in range(length))

def rand_nhi():
    letters = ''.join(choice(string.uppercase) for i in range(3))
    digits =  ''.join(choice(string.digits) for i in range(3))
    return letters + digits

def rand_bool():
    return choice(['Yes', 'No'])

def write_to_file(filename, data):
    f = open(filename, 'w')
    f.writelines(data)
    f.close

patient_id = randrange(0, 100000)
firstname = rand_lower_str(10).capitalize()
lastname = rand_lower_str(10).capitalize()
nhi = rand_nhi()
occupation = rand_lower_str(20).capitalize()
citizen_resident = 'Yes'
contact_num = randrange(100000, 999999)
gender = choice(['Male', 'Female'])
dob = rand_lower_str(20)

vital_info_id = randrange(0, 10000000)
vital_info_url = "/patients/%s/vitalinfo" % patient_id
weight_value = rand_lower_str(20)
weight_unit = choice(['kg', 'lb'])
height_value = rand_lower_str(20)
height_unit = choice(['cm'])
blood_type = rand_lower_str(20)
smoker = rand_lower_str(20)
drinker = rand_lower_str(20)
family_hist = rand_lower_str(20)
overseas_recently = rand_lower_str(20)
overseas_destinations = rand_lower_str(20)
medical_conditions = rand_lower_str(20)
allergies = rand_lower_str(20)

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
