#!/usr/bin/env python

from flask import Flask, request, jsonify
import data

app = Flask(__name__)


@app.route('/patients')
def patients():
    if request.method == "GET":
        return jsonify(data.get_patients())

    elif request.method == "POST":
        data.store_patient(request.json)


@app.route('/patients/<int:patient_id>', methods=['GET', 'POST'])
def patient(patient_id):
    if request.method == "GET":
        return jsonify(data.get_patient(patient_id))

    elif request.method == "PUT":
        data.update_patient(patient_id, request.json)

    elif request.method == "DELETE":
        data.delete_patient(patient_id)


@app.route('/patients/<int:patient_id>/vitalinfos')
def vital_infos(patient_id):
    if request.method == "GET":
        return jsonify(data.get_vital_infos(patient_id))

    elif request.method == "POST":
        data.store_vital_info(patient_id, request.json)


@app.route('/patients/<int:patient_id>/vitalinfos/<int:vitalinfo_id>', methods=['GET', 'POST'])
def vital_info(patient_id, vitalinfo_id):
    if request.method == "GET":
        return jsonify(data.get_vital_info(patient_id, vitalinfo_id))

    elif request.method == "PUT":
        data.update_vital_info(patient_id, vitalinfo_id, request.json)

    elif request.method == "DELETE":
        data.delete_vital_info(vitalinfo_id)


if __name__ == '__main__':
    app.run(debug=True)
