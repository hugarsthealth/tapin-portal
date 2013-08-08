import json

from flask import request, redirect, url_for, jsonify, render_template, make_response
from sqlalchemy import desc

from server import app
from models import db, Patient, CheckIn, Department, Appointment


@app.route('/')
def root():
    # serve up the angular
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    resp = make_response(redirect(url_for('root')))

    if 'department' in request.form:
        resp.set_cookie('department', request.form.get('department'))
    else:
        return make_response("'department' not in POST data. Received: {}".format(
            json.dumps(request.form, indent=2)), 400)

    return resp


@app.route('/departments', methods=['GET'])
def departments():
    return make_response((json.dumps([
        d.serialize() for d in Department.query.all()
    ]), 200, {"Content-Type": "application/json"}))


@app.route('/departments/<int:department_id>', methods=['GET'])
def department(department_id):
    return jsonify(Department.query.get(department_id).serialize())


@app.route('/patients', methods=['GET', 'POST'])
def patients():
    query = Patient.query.join(Department.patients).filter(
        Department.department_name == request.cookies.get('department', 'default'))

    if request.method == "GET":
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 100))

        return make_response((json.dumps([
            p.serialize() for p in query
            .order_by(desc(Patient.latest_checkin_time))
            .offset(offset)
            .limit(limit)
            .all()
        ]), 200, {"Content-Type": "application/json"}))

    elif request.method == "POST":
        patient_data = json.loads(request.data)
        patient = Patient(**patient_data)
        patient = db.merge(patient)
        db.commit()

        department = Department.query.filter_by(
            department_name=request.cookies.get('department', 'default')).first()

        if department:
            patient.departments.append(department)

        db.commit()

        if 'checkin' in patient_data:
            add_checkin(patient.nhi, patient_data['checkin'])

        return jsonify(patient.serialize())


@app.route('/patients/<nhi>', methods=['GET', 'PUT', 'DELETE'])
def patient(nhi):
    patient = Patient.query.filter_by(nhi=nhi).first()

    if not patient:
        return make_response("No patient with NHI " + nhi, 404)

    elif request.method == "GET":
        return jsonify(patient.serialize())

    elif request.method == "DELETE":
        db.delete(patient)
        db.commit()

        return make_response("Deleted patient: {}".format(nhi), 200)


@app.route('/patients/<nhi>/checkins', methods=['GET', 'POST'])
def checkins(nhi):
    if request.method == "GET":
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 100))

        return make_response((json.dumps([
            v.serialize() for v in CheckIn.query
            .filter_by(patient_nhi=nhi)
            .order_by(desc(CheckIn.checkin_time))
            .offset(offset)
            .limit(limit)
        ]), 200, {"Content-Type": "application/json"}))

    elif request.method == "POST":
        return jsonify(add_checkin(nhi, json.loads(request.data)).serialize())


@app.route('/patients/<nhi>/checkins/<int:checkin_id>', methods=['GET', 'POST', 'DELETE'])
def checkin(nhi, checkin_id):
    checkin = CheckIn.query.filter_by(
        patient_nhi=nhi, checkin_id=checkin_id).first()

    if not checkin:
        return make_response("No checkin for patient {} with id {}".format(nhi, checkin_id))

    elif request.method == "GET":
        return jsonify(checkin.serialize())

    elif request.method == "POST":
        checkin_data = json.loads(request.data)
        checkin = CheckIn(**checkin_data)
        checkin.checkin_id = checkin_id
        checkin = db.merge(checkin)
        db.commit()

        return jsonify(checkin.serialize())

    elif request.method == "DELETE":
        db.delete(checkin)
        db.commit()

        return make_response("Deleted checkin: {} from patient: {}".format(checkin_id, nhi), 200)


@app.route('/patients/<nhi>/appointments', methods=['GET', 'POST'])
def patient_appointments(nhi):
    if request.method == "GET":
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 100))

        return make_response((json.dumps([
            a.serialize() for a in Appointment.query
            .filter_by(patient_nhi=nhi)
            .order_by(desc(Appointment.time))
            .offset(offset)
            .limit(limit)
        ]), 200, {"Content-Type": "application/json"}))

    elif request.method == "POST":
        appointment = Appointment(**json.loads(request.data))
        db.commit()

        return jsonify(appointment.serialize())


@app.route('/patients/<nhi>/appointments/<int:appointment_id>', methods=['GET', 'POST', 'DELETE'])
def patient_appointment(nhi, appointment_id):
    appointment = Appointment.query.filter_by(
        patient_nhi=nhi, appointment_id=appointment_id).first()

    if not appointment:
        return make_response("No appointment for patient {} with id {}".format(nhi, appointment_id))

    elif request.method == "GET":
        return jsonify(appointment.serialize())

    elif request.method == "POST":
        appointment_data = json.loads(request.data)
        appointment = Appointment(**appointment_data)
        appointment.appointment_id = appointment_id
        appointment = db.merge(appointment)
        db.commit()

        return jsonify(appointment.serialize())

    elif request.method == "DELETE":
        db.delete(appointment)
        db.commit()

        return make_response("Deleted appointment: {} from patient: {}".format(appointment_id, nhi), 200)

@app.route('/patient_summaries')
def patient_summaries():
    return json.dumps([summarize_patient(p) for p in Patient.query.all()])

def summarize_patient(patient):
    try:
        return {
            "nhi" : patient.nhi,
            "name": full_name_from_checkin(patient.checkins[0])
        }
    except IndexError:
        print patient.nhi
        return



def full_name_from_checkin(checkin):
    return checkin.firstname + " " + checkin.lastname


@app.route('/appointments', methods=['GET'])
def appointments():
    return make_response((json.dumps([
        d.serialize() for d in Appointment.query
        .order_by(desc(Appointment.time))
        .all()
    ]), 200, {"Content-Type": "application/json"}))


@app.route('/appointments/<int:appointment_id>', methods=['GET'])
def appointment(appointment_id):
    return jsonify(Appointment.query.get(appointment_id).serialize())


def add_checkin(nhi, data):
    c = CheckIn(**data)
    c.patient_nhi = nhi

    db.add(c)
    db.commit()

    if c.patient.latest_checkin_time is None or c.checkin_time > c.patient.latest_checkin_time:
        c.patient.latest_checkin_time = c.checkin_time

    db.commit()
    return c
