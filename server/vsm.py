import json
import datetime

from flask import request, jsonify, url_for, redirect, render_template, make_response

from server import app
from models import db, Patient, VitalInfo


@app.route('/')
def root():
    # serve up the angular
    return render_template('index.html')


@app.route('/patients/', methods=['GET', 'POST'])
def patients():
    if request.method == "GET":
        start = int(request.args.get('offset', 0))
        end = start + int(request.args.get('limit', 100))
        return jsonify({'patients': [p.serialize() for p in Patient.query.slice(start, end)]})

    elif request.method == "POST":
        p = Patient(**json.loads(request.data))
        db.add(p)
        db.commit()
        return redirect(url_for('patient', patient_id=p.patient_id))


@app.route('/patients/<nhi>/', methods=['GET', 'PUT', 'DELETE'])
def patient(nhi):
    if request.method == "GET":
        return jsonify({'patient': Patient.query.get(nhi).serialize()})

    elif request.method == "PUT":
        patient = Patient.query.get(nhi)
        patient.__init__(**json.loads(request.data))

        db.commit()

    elif request.method == "DELETE":
        db.delete(Patient.query.get(nhi))

        db.commit()


@app.route('/patients/<nhi>/vitalinfos/', methods=['GET', 'POST'])
def vital_infos(nhi):
    if request.method == "GET":
        start = int(request.args.get('offset', 0))
        end = start + int(request.args.get('limit', 100))
        return jsonify({'vitalinfos': [v.serialize() for v in VitalInfo.query.filter_by(patient_nhi=nhi).slice(start, end)]})

    elif request.method == "POST":
        v = VitalInfo(**json.loads(request.data))

        v.patient_nhi = nhi
        v.check_in_time = datetime.datetime.strptime(v.check_in_time, "%Y-%m-%dT%H:%M:%S.%f")

        db.add(v)
        db.commit()

        if v.patient.last_check_in is None or v.check_in_time > v.patient.last_check_in:
            v.patient.last_check_in = v.check_in_time  # untested sqlalchemy magic

        db.commit()
        return redirect(url_for('vital_info', patient_id=v.patient_id, vital_info_id=v.vital_info_id))


@app.route('/patients/<nhi>/vitalinfos/<int:vital_info_id>/', methods=['GET', 'PUT', 'DELETE'])
def vital_info(nhi, vital_info_id):
    if request.method == "GET":
        vitalinfo = VitalInfo.query.filter_by(patient_nhi=nhi, vital_info_id=vital_info_id).first()
        return jsonify({'vitalinfo': vitalinfo.serialize()})

    elif request.method == "PUT":
        data = json.loads(request.data)
        data['check_in_time'] = datetime.datetime.strptime(data['check_in_time'], "%Y-%m-%dT%H:%M:%S.%f")
        VitalInfo.query.filter_by(patient_nhi=nhi, vital_info_id=vital_info_id).update(data)

        db.commit()
        return make_response("Successfully updated!", 200)

    elif request.method == "DELETE":
        vitalinfo = VitalInfo.query.filter_by(patient_nhi=nhi, vital_info_id=vital_info_id).first()
        db.delete(vitalinfo)

        db.commit()
        return make_response("Successfully deleted!", 200)
