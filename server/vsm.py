import json
from server import app
from data import data
from flask import request, jsonify, render_template


@app.route('/')
def root():
    #serve up the angular
    return render_template('index.html')


@app.route('/patients/', methods=['GET', 'POST'])
def patients():
    if request.method == "GET":
        return jsonify(data.get_patients())

    elif request.method == "POST":
        # data.store_patient(request.data)
        return request.data


@app.route('/patients/<int:patient_id>/', methods=['GET', 'PUT', 'DELETE'])
def patient(patient_id):
    if request.method == "GET":
        return jsonify(data.get_patient(patient_id))

    elif request.method == "PUT":
        data.update_patient(patient_id, request.json)

    elif request.method == "DELETE":
        data.delete_patient(patient_id)


@app.route('/patients/<int:patient_id>/vitalinfos/', methods=['GET', 'POST'])
def vital_infos(patient_id):
    if request.method == "GET":
        return jsonify(data.get_vital_infos(patient_id))

    elif request.method == "POST":
        data.store_vital_info(patient_id, request.json)


@app.route('/patients/<int:patient_id>/vitalinfos/<int:vital_info_id>/', methods=['GET', 'PUT', 'DELETE'])
def vital_info(patient_id, vital_info_id):
    if request.method == "GET":
        return jsonify(data.get_vital_info(patient_id, vital_info_id))

    elif request.method == "PUT":
        data.update_vital_info(patient_id, vital_info_id, request.json)

    elif request.method == "DELETE":
        data.delete_vital_info(vital_info_id)
