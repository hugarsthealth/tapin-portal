import json
import datetime

from server import app, db
from flask import request, jsonify, url_for, redirect, render_template
from models.patient import Patient
from models.vitalinfo import VitalInfo


@app.route('/')
def root():
    #serve up the angular
    return render_template('index.html')


@app.route('/patients/', methods=['GET', 'POST'])
def patients():
    if request.method == "GET":
        start = int(request.args.get('offset', 0))
        end = start + int(request.args.get('limit', 100))
        return jsonify({'patients': [p.serialize() for p in Patient.query.slice(start,end)]})

    elif request.method == "POST":
        p = Patient(**json.loads(request.data))
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('patient', patient_id=p.patient_id))


@app.route('/patients/<nhi>/', methods=['GET', 'PUT', 'DELETE'])
def patient(nhi):
    if request.method == "GET":
        return jsonify({'patient': Patient.query.get_or_404(nhi).serialize()})

    elif request.method == "PUT":
        patient = Patient.query.get_or_404(nhi)
        patient.__init__(**json.loads(request.data))

        db.session.commit()

    elif request.method == "DELETE":
        db.session.delete(Patient.query.get_or_404(nhi))

        db.session.commit()


@app.route('/patients/<nhi>/vitalinfos/', methods=['GET', 'POST'])
def vital_infos(nhi):
    if request.method == "GET":
        start = int(request.args.get('offset', 0))
        end = start + int(request.args.get('limit', 100))
        return jsonify({'vitalinfos': [v.serialize() for v in VitalInfo.query.filter_by(patient_nhi=nhi).slice(start,end)]})

    elif request.method == "POST":
        v = VitalInfo(**json.loads(request.data))

        v.patient_nhi = nhi
        v.check_in_time = datetime.datetime.strptime(v.check_in_time, "%Y-%m-%dT%H:%M:%S.%f")

        db.session.add(v)
        db.session.commit()

        if v.patient.last_check_in is None or v.check_in_time > v.patient.last_check_in:
            v.patient.last_check_in = v.check_in_time  # untested sqlalchemy magic

        db.session.commit()
        return redirect(url_for('vital_info', patient_id=v.patient_id, vital_info_id=v.vital_info_id))


@app.route('/patients/<nhi>/vitalinfos/<int:vital_info_id>/', methods=['GET', 'PUT', 'DELETE'])
def vital_info(nhi, vital_info_id):
    if request.method == "GET":
        return jsonify({'vitalinfo': VitalInfo.query.get_or_404(vital_info_id).serialize()})

    elif request.method == "PUT":
        vitalinfo = VitalInfo.query.get_or_404(vital_info_id)
        vitalinfo.__init__(**json.loads(request.data))

        db.session.commit()

    elif request.method == "DELETE":
        db.session.delete(VitalInfo.query.get_or_404(vital_info_id))

        db.session.commit()
