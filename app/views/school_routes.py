from app import app, db
from flask import render_template, redirect, url_for, request, jsonify, abort, session
import app.controllers.school_controller as scc
from app.models.templates import *
import os
import json
from app.forms import SigninForm, SignUpForm
from flask_api import status
from werkzeug.security import generate_password_hash, check_password_hash

success = (True, "success")
fail = (False, "failed")

def binary_response_builder(result, message):
    if result[0]:
        message["status_code"] = 200
        resp = status.HTTP_200_OK
    else:
        message["status_code"] = 500
        message["message"] = result[1]
        resp = status.HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify(message), resp

"""
Org CRUD routes
"""

@app.route("/get_all_schools/<int:offset>/<int:size>", methods=["GET"])
def get_all_schools(offset, size):
    schools = scc.get_all_schools(offset, size)
    message = {"data": schools}
    resp = binary_response_builder(success, message)
    return resp

@app.route("/get_school_using_id", methods=["POST"])
def get_school_using_id():
    json_request = request.get_json()
    data = json_request['data']
    school_id = data['school_id']
    school = scc.get_school_using_id(school_id)
    message = {"data": school}
    resp = binary_response_builder(success,message)
    return resp

@app.route("/upsert_school", methods=["POST"])
def create_school():
    json_request = request.get_json()
    data = json_request["data"]
    resp = binary_response_builder(scc.upsert_school(data), {})
    return resp

@app.route("/search_school/<search>", methods=["GET"])
def search_school(search):
    schools = scc.search_school(search)
    message = {"data": schools}
    resp = binary_response_builder(success, message)
    return resp

@app.route("/update_school", methods=["POST"])
def update_school():
    json_request = request.get_json()
    data = json_request["data"]
    school_id = data['school_id']
    update_dict = data['update_dict']
    resp = binary_response_builder(
        scc.update_school(school_id, update_dict), {})
    return resp

   # data = json_request["data"]
    #resp = binary_response_builder(
     #   scc.update_school(data["administrator_id"], data), {})
    #return resp

@app.route("/get_school", methods=["POST"])
def get_school():
    json_request = request.get_json()
    data = json_request["data"]
    res = scc.get_school(data["administrator_id"])
    resp = binary_response_builder(res, {"schools": res[1], "school_id": res[1]})
    return resp

@app.route("/delete_school", methods=["POST"])
def delete_school():
    json_request = request.get_json()
    data = json_request["data"]  
    res = scc.delete_school(data['school_id'])  
    #res = scc.delete_school(data["administrator_id"])
    resp = binary_response_builder(res, {})
    return resp


@app.route("/add_student_to_school", methods=["POST"])
def add_student_to_school():
    json_request = request.get_json()
    data = json_request["data"]
    student_ids = data["student_id"]
    school_id = data["school_id"]
    for student_id in student_ids:
        scc.add_student_to_school(student_id, school_id)
    resp = binary_response_builder(success, {})
    return resp


@app.route("/delete_student_from_school", methods=["POST"])
def delete_student_from_school():
    json_request = request.get_json()
    data = json_request["data"]
    student_ids = data["student_id"]
    school_id = data["school_id"]
    for student_id in student_ids:
        scc.delete_student_from_school(student_id, section_id)
    resp = binary_response_builder(success, {})
    return resp

