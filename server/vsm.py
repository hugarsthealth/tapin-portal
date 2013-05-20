import json

from flask import request, redirect, url_for, jsonify, render_template, make_response
from sqlalchemy import desc

from server import app
from models import db, Patient, VitalInfo, Department


@app.route('/')
def root():
    # serve up the angular
    return render_template('index.html')


@app.route('/login/', methods=['POST'])
def login():
    resp = make_response(redirect(url_for('root')))

    if 'department' in request.values:
        resp.set_cookie('department', request.form.get('department'))
    else:
        return make_response("'department' not in POST data. Received: {}".format(
            json.dumps(request.form, indent=2)), 400)

    return resp


@app.route('/patients/', methods=['GET', 'POST'])
def patients():
    query = Patient.query.join(Department.patients).filter(
        Department.department_name == request.cookies.get('department', 'default'))

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
        patient = db.merge(patient)
        db.commit()

        department = Department.query.filter_by(
            department_name=request.cookies.get('department', 'default')).first()

        if department:
            patient.departments.append(department)

        db.commit()

        if 'vitalinfo' in patient_data:
            add_vital_info(patient.nhi, patient_data['vitalinfo'])

        return make_response("Added patient: {}".format(json.dumps(patient.serialize())), 200)


@app.route('/patients/<nhi>/', methods=['GET', 'PUT', 'DELETE'])
def patient(nhi):
    patient = Patient.query.join(Department.patients).filter(
        Department.department_name == request.cookies.get('department', 'default')
    ).filter_by(nhi=nhi).first()

    if not patient:
        return make_response("No patient with NHI " + nhi, 404)

    elif request.method == "GET":
        return jsonify({'patient': patient.serialize()})

    elif request.method == "DELETE":
        db.delete(patient)
        db.commit()

        return make_response("Deleted patient: {}".format(nhi), 200)


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
        v = add_vital_info(nhi, json.loads(request.data))
        return make_response("Added vitalinfo: {}".format(json.dumps(v.serialize())), 200)


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
        vitalinfo = VitalInfo(**vitalinfo_data)
        vitalinfo.vital_info_id = vital_info_id
        vitalinfo = db.merge(vitalinfo)
        db.commit()

        return make_response("Updated vitalinfo: {}".format(json.dumps(vitalinfo.serialize())), 200)

    elif request.method == "DELETE":
        db.delete(vitalinfo)
        db.commit()

        return make_response("Deleted vitalinfo: {} from patient: {}".format(vital_info_id, nhi), 200)


def add_vital_info(nhi, data):
    v = VitalInfo(**data)
    v.patient_nhi = nhi

    db.add(v)
    db.commit()

    if v.patient.latest_check_in is None or v.check_in_time > v.patient.latest_check_in:
        v.patient.latest_check_in = v.check_in_time

    db.commit()
    return v
