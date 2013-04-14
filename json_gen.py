#!/usr/bin/env python

import json
from random import choice, randrange
import string

def rand_lower_str(length):
    return ''.join(choice(string.lowercase) for i in range(length))

def rand_nhi(length):
    return ''.join(choice(string.uppercase + string.digits) for i in range(length))

def rand_bool():
    return choice(['Yes', 'No'])

firstname = rand_lower_str(10).capitalize()
lastname = rand_lower_str(10).capitalize()
nhi = rand_nhi(6)
occupation = rand_lower_str(20).capitalize()
citizen_resident = 'Yes'
contact_num = randrange(100000, 999999)
gender = choice(['Male', 'Female'])
dob = rand_lower_str(20)
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
    'firstname': firstname,
    'lastname': lastname,
    'nhi': nhi,
    'occupation': occupation,
    'citizen_resident': citizen_resident,
    'contact_num': contact_num,
    'gender': gender,
    'dob': dob,
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

j = json.dumps(patient, sort_keys=True, indent=4)
print(j)
