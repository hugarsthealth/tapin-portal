import json

from flask import request, redirect, url_for, session, jsonify, render_template, make_response
from sqlalchemy import desc

from server import app
from models import db, Patient, VitalInfo


@app.route('/')
def root():
    # serve up the angular
    return render_template('index.html')


@app.route('/login/', methods=['POST'])
def login():
    print "Tryna login"
    if 'role' in request.form:
        print request.form['role']
        session['role'] = request.form['role']
        

    return redirect(url_for('root'))


@app.route('/patients/', methods=['GET', 'POST'])
def patients():
    if request.method == "GET":
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 100))

        return jsonify({'patients': [
            p.serialize() for p in Patient.query
            .order_by(desc(Patient.latest_check_in))
            .offset(offset)
            .limit(limit)
            .all()
        ]})

    elif request.method == "POST":
        patient_data = json.loads(request.data)
        patient = Patient(**patient_data)
        db.add(patient)
        db.commit()

        if 'vitalinfo' in patient_data:
            add_vital_info(patient.nhi, patient_data['vitalinfo'])

        return make_response("Successfully added!", 200)


@app.route('/patients/<nhi>/', methods=['GET', 'PUT', 'DELETE'])
def patient(nhi):
    patient = Patient.query.get(nhi)

    if not patient:
        return make_response("No patient with NHI " + nhi, 404)

    elif request.method == "GET":
        return jsonify({'patient': patient.serialize()})

    elif request.method == "POST":
        patient.deserialize(json.loads(request.data))
        db.commit()

        return make_response("Successfully updated!", 200)

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


@app.route('/patients/<nhi>/vitalinfos/<int:vital_info_id>/', methods=['GET', 'PUT', 'DELETE'])
def vital_info(nhi, vital_info_id):
    vitalinfo = VitalInfo.query.filter_by(
        patient_nhi=nhi, vital_info_id=vital_info_id).first()

    if not vitalinfo:
        return make_response("No vitalinfo for patient {} with id {}".format(nhi, vital_info_id))

    elif request.method == "GET":
        return jsonify({'vitalinfo': vitalinfo.serialize()})

    elif request.method == "POST":
        vitalinfo.deserialize(json.loads(request.data))
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
