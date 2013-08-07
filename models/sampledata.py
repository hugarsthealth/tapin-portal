#!/usr/bin/env python

from random import choice, randrange, getrandbits, randint
from datetime import datetime, timedelta
import string

from models import db, Patient, CheckIn, Department, Appointment

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


def generate_patient():
    nhi = rand_nhi()

    return {
        'nhi': nhi,
    }


def generate_checkin():
    checkin_time = rand_date()
    firstname = rand_name()
    lastname = rand_name()
    occupation = rand_name()
    citizen_resident = rand_bool()
    contact_num = rand_digit_str(10)
    gender = choice(['Male', 'Female'])
    dob = rand_date(30000)
    weight_value = randrange(0, 200)
    weight_unit = choice(['kg', 'lb'])
    height_value = randrange(0, 200)
    height_unit = choice(['cm'])
    blood_type = choice(['A', 'B', 'AB', 'O'])
    smoker = rand_bool()
    drinker = rand_bool()
    family_hist = list_of_rand_sentences(4, 10)
    overseas_recently = rand_bool()
    overseas_dests = list_of_rand_sentences(3, 2)
    medical_conditions = list_of_rand_sentences(2, 8)
    allergies = list_of_rand_sentences(4, 2)
    location = rand_name()

    return {
        'checkin_time': checkin_time,
        'firstname': firstname,
        'lastname': lastname,
        'occupation': occupation,
        'citizen_resident': citizen_resident,
        'contact_num': contact_num,
        'gender': gender,
        'dob': dob,
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
        'allergies': allergies,
        'location': location
    }


def generate_appointment():
    return dict(
        time = rand_date(),
        reason = rand_sentence(5),
        location = "Starhip Children's Hospital"
    )


def populate_database(num_patients, min_checkins, max_checkins):
    """
    Generates a number of Patients and a number of CheckIns per patient and
    stores them in the database.

    Arguments
    num_patients    -- the number of patients to generate
    min_checkins -- the minimum number of CheckIns to generate per Patient
    max_checkins -- the maximum number of CheckIns to generate per Patient

    """
    departments = [
        Department(department_name="Cardiology"),
        Department(department_name="Emergency"),
        Department(department_name="Gynecology"),
        Department(department_name="Pediatrics"),
        Department(department_name="Obstetrics"),
        Department(department_name="Oncology"),
        Department(department_name="Orthopedics"),
        Department(department_name="Neurology")
    ]

    for i in xrange(num_patients):
        patient = Patient(**generate_patient())
        patient.departments.append(choice(departments))
        db.add(patient)

        for j in xrange(randrange(min_checkins, max_checkins)):
            checkin = CheckIn(**generate_checkin())
            checkin.patient_nhi = patient.nhi

            lci = patient.latest_checkin_time
            vid = checkin.checkin_time

            lci = vid if lci is None or vid > lci else lci
            patient.latest_checkin_time = lci

            db.add(checkin)

        for k in xrange(randrange(0, 3)):
            appointment = Appointment(**generate_appointment())
            appointment.patient_nhi = patient.nhi

            db.add(appointment)

    db.commit()
