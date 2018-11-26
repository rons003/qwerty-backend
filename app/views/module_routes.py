from app import app, db
from flask import render_template, redirect, url_for, request, jsonify, abort, session
import app.controllers.module_controller as moc
import app.controllers.section_controller as sec
import app.controllers.user_controller as uc
import app.controllers.chapter_controller as chc
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


@app.route("/get_all_modules/<int:offset>/<int:size>", methods=["GET"])
def get_all_modules(offset, size):
    modules = moc.get_all_modules(offset, size)
    message = {"data": modules}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/create_module", methods=["POST"])
def create_module():
    json_request = request.get_json()
    data = json_request["data"]
    resp = binary_response_builder(moc.create_module(data), {})
    return resp


@app.route("/update_module", methods=["POST"])
def update_module():
    json_request = request.get_json()
    data = json_request["data"]
    module_id = data["module_id"]
    update_dict = data["update_dict"]
    resp = binary_response_builder(moc.update_module(module_id,
                                                     update_dict), {})
    return resp


@app.route("/get_module", methods=["POST"])
def get_module():
    json_request = request.get_json()
    data = json_request["data"]
    modules = moc.get_module(data["school_id"])
    message = {"data": modules}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/get_module_using_id", methods=["POST"])
def get_module_using_id():
    json_request = request.get_json()
    data = json_request["data"]
    modules = moc.get_module_using_id(data["module_id"])
    message = {"data": modules}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/delete_module", methods=["POST"])
def delete_module():
    json_request = request.get_json()
    data = json_request["data"]
    module_ids = data["module_id"]
    for mod_id in module_ids:
        moc.delete_module(mod_id)
    resp = binary_response_builder(success, {})
    return resp


@app.route("/get_section_from_module", methods=["POST"])
def get_section_from_module():
    json_request = request.get_json()
    data = json_request["data"]
    modules = moc.get_module_using_id(data["module_id"])
    section_data = []
    message = {}
    for sec_id in modules.section_list:
        section_data.append(sec.get_section_using_id(sec_id))
    message["data"] = section_data
    resp = binary_response_builder(success, message)
    return resp


@app.route("/add_section_to_module", methods=["POST"])
def add_section_to_module():
    json_request = request.get_json()
    data = json_request["data"]
    section_id = data["section_id"]
    module_id = data["module_id"]
    resp = binary_response_builder(
        moc.add_section_to_module(section_id, module_id), {})
    return resp


@app.route("/delete_section_from_module", methods=["POST"])
def delete_section_from_module():
    json_request = request.get_json()
    data = json_request["data"]
    section_ids = data["section_id"]
    module_id = data["module_id"]
    resp = binary_response_builder(
        moc.delete_section_from_module(section_ids, module_id), {})
    return resp

@app.route("/get_chapter_from_module", methods=["POST"])
def get_chapter_from_module():
    json_request = request.get_json()
    data = json_request["data"]
    modules = moc.get_module_using_id(data["module_id"])
    chapter_data = []
    for chap_id in modules.chapter_list:
        chapter_data.append(chc.get_chapter_using_id(chap_id))
    message  = { "data": chapter_data }
    resp = binary_response_builder(success, message)
    return resp


@app.route("/add_chapter_to_module", methods=["POST"])
def add_chapter_to_module():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_id = data["chapter_id"]
    module_id = data["module_id"]
    resp = binary_response_builder(
        moc.add_chapter_to_module(chapter_id, module_id), {})
    return resp


@app.route("/delete_chapter_from_module", methods=["POST"])
def delete_chapter_from_module():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_ids = data["chapter_id"]
    module_id = data["module_id"]
    resp = binary_response_builder(
        moc.delete_chapter_from_module(chapter_ids, module_id), {})
    return resp
