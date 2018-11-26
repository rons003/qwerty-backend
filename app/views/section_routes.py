from app import app, db
from flask import render_template, redirect, url_for, request, jsonify, abort, session
import app.controllers.section_controller as sec
import app.controllers.user_controller as usec
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


@app.route("/get_all_sections/<int:offset>/<int:size>", methods=["GET"])
def get_all_sections(offset, size):
    sections = sec.get_all_sections(offset, size)
    message = {"data": sections}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/search_section/<search>", methods=["GET"])
def search_section(search):
    section = sec.search_section(search)
    message = {"data": section}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/create_section", methods=["POST"])
def create_section():
    json_request = request.get_json()
    data = json_request["data"]
    resp = binary_response_builder(sec.create_section(data), {})
    return resp


@app.route("/update_section", methods=["POST"])
def update_section():
    json_request = request.get_json()
    data = json_request["data"]
    section_id = data["section_id"]
    update_dict = data["update_dict"]
    resp = binary_response_builder(
        sec.update_section(section_id, update_dict), {})
    return resp


@app.route("/get_section_using_id", methods=["POST"])
def get_section_using_id():
    json_request = request.get_json()
    data = json_request["data"]
    sections = sec.get_section_using_id(data["section_id"])
    message = {"data": sections}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/get_section", methods=["POST"])
def get_section():
    json_request = request.get_json()
    data = json_request["data"]
    sections = sec.get_section(data["school_id"])
    message = {"data": sections}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/delete_section", methods=["POST"])
def delete_section():
    json_request = request.get_json()
    data = json_request["data"]
    secion_ids = data["section_id"]
    for sec_id in secion_ids:
        sec.delete_section(sec_id)
    resp = binary_response_builder(success, {})
    return resp


@app.route("/get_student_from_section", methods=["POST"])
def get_student_from_section():
    json_request = request.get_json()
    data = json_request["data"]
    sections = sec.get_section_using_id(data["section_id"])
    student_data = []
    message = {}
    for user_id in sections.student_list:
        student_data.append(usec.get_user(user_id))
    message["data"] = student_data
    resp = binary_response_builder(success, message)
    return resp


@app.route("/add_student_to_section", methods=["POST"])
def add_student_to_section():
    json_request = request.get_json()
    data = json_request["data"]
    student_ids = data["student_id"]
    section_id = data["section_id"]
    resp = binary_response_builder(
        sec.add_student_to_section(student_ids, section_id), {})
    return resp


@app.route("/delete_student_from_section", methods=["POST"])
def delete_student_from_section():
    json_request = request.get_json()
    data = json_request["data"]
    student_ids = data["student_id"]
    section_id = data["section_id"]
    resp = binary_response_builder(
        sec.delete_student_from_section(student_ids, section_id), {})
    return resp


@app.route("/get_student_from_school", methods=["POST"])
def get_student_from_school():
    json_request = request.get_json()
    data = json_request["data"]
    students = sec.get_student_from_school(data["school_id"])
    message = {"data": students}
    resp = binary_response_builder(success, message)
    return resp
