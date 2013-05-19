import json

from flask import request, redirect, url_for, session, jsonify, render_template, make_response
from sqlalchemy import desc

from server import app
from models import db, Patient, VitalInfo, Department


@app.route('/')
def root():
    # serve up the angular
    return render_template('index.html')


@app.route('/login/', methods=['POST'])
def login():
    if 'department' in request.form:
        session['department'] = request.form['department']
    else:
        return make_response("'department' not in POST data. Received: {}".format(
            json.dumps(request.form, indent=2)), 400)

    return redirect(url_for('root'))


@app.route('/patients/', methods=['GET', 'POST'])
def patients():
    query = Patient.query.join(Department.patients).filter(
        Department.department_name == session.get('department', 'default'))

    if request.method == "GET":
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 100))

        return jsonify({'patients': [
            p.serialize() for p in query
            .order_by(desc(Patient.latest_check_in))
            .offset(offset)
            .limit(limit)
            .all()
        ]})

    elif request.method == "POST":
        patient_data = json.loads(request.data)
        patient = Patient(**patient_data)
        patient = db.merge(Patient.query.get(patient.nhi))

        department = Department.query.filter_by(
            department_name=session.get('department', 'default')).first()
        patient.departments.append(department)

        db.add(patient)
        db.commit()

        if 'vitalinfo' in patient_data:
            add_vital_info(patient.nhi, patient_data['vitalinfo'])

        return make_response("Successfully added!", 200)


@app.route('/patients/<nhi>/', methods=['GET', 'PUT', 'DELETE'])
def patient(nhi):
    patient = Patient.query.join(Department.patients).filter(
        Department.department_name == session.get('department', 'default')).get(nhi)

    if not patient:
        return make_response("No patient with NHI " + nhi, 404)
    else:
        patient = Patient.query.get(patient.nhi)

    if request.method == "GET":
        return jsonify({'patient': patient.serialize()})

    elif request.method == "DELETE":
        db.delete(patient)
        db.commit()

        return make_response("Successfully deleted!", 200)


@app.route('/patients/<nhi>/vitalinfos/', methods=['GET', 'POST'])
def vital_infos(nhi):
    if request.method == "GET":
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 100))

        return jsonify({'vitalinfos': [
            v.serialize() for v in VitalInfo.query
            .filter_by(patient_nhi=nhi)
            .order_by(desc(VitalInfo.check_in_time))
            .offset(offset)
            .limit(limit)
        ]})

    elif request.method == "POST":
        add_vital_info(nhi, json.loads(request.data))

        return make_response("Successfully added!", 200)


@app.route('/patients/<nhi>/vitalinfos/<int:vital_info_id>/', methods=['GET', 'POST', 'DELETE'])
def vital_info(nhi, vital_info_id):
    vitalinfo = VitalInfo.query.filter_by(
        patient_nhi=nhi, vital_info_id=vital_info_id).first()

    if not vitalinfo:
        return make_response("No vitalinfo for patient {} with id {}".format(nhi, vital_info_id))

    elif request.method == "GET":
        return jsonify({'vitalinfo': vitalinfo.serialize()})

    elif request.method == "POST":
        vitalinfo_data = json.loads(request.data)
        new_vitalinfo = VitalInfo(**vitalinfo_data)
        new_vitalinfo.nhi = nhi
        new_vitalinfo.vital_info_id = vital_info_id
        merged_vitalinfo = db.merge(new_vitalinfo)
        db.commit()

        return make_response("Successfully updated!", 200)

    elif request.method == "DELETE":
        db.delete(vitalinfo)
        db.commit()

        return make_response("Successfully deleted!", 200)


def add_vital_info(nhi, data):
    v = VitalInfo(**data)
    v.patient_nhi = nhi

    db.add(v)
    db.commit()

    if v.patient.latest_check_in is None or v.check_in_time > v.patient.latest_check_in:
        v.patient.latest_check_in = v.check_in_time

    db.commit()
