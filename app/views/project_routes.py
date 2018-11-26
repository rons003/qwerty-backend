from app import app, db
from flask import render_template, redirect, url_for, request, jsonify, abort, session
import app.controllers.group_controller as gc
import app.controllers.challenge_controller as cc
import app.controllers.user_controller as uc
import app.controllers.chapter_controller as chc
import app.controllers.project_controller as pc
from app.models.templates import *
import os, json
from flask_api import status

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

def get_keys_from_data(data_dict, *args):
    """
    Retrieves a list of key parameters from the data
    dictionary. This data dictionary comes from a
    request object that is posted to one of the endpoints

    Example:
        I want to update a user via /update_user
        data = json_request["data"]
        params = get_keys_from_data(data, "user_id", "update_dict")
        res = uc.update_user(**params)
    """
    params = []
    for arg in args:
        try:
            params.append(int(data_dict[arg]))
        except:
            params.append(data_dict[arg])
    return params

@app.route("/get_all_projects_of_user", methods=["POST"])
def get_all_projects_of_user():
    """
    Gets all projects that belongs to a user
    """
    json_request = request.get_json()
    print json_request
    data = json_request["data"]
    user_id = data["user_id"]
    message = {"projects": pc.get_all_projects_of_user(user_id)}
    resp = binary_response_builder(success, message)
    return resp

@app.route("/get_all_projects_of_group", methods=["POST"])
def get_all_projects_of_group():
    """
    Gets all projects that belongs to a group
    """
    json_request = request.get_json()
    print json_request
    data = json_request["data"]
    group_id = data["group_id"]
    student_ids = gc.get_students(group_id)
    message = {"projects": pc.get_all_projects_of_group(student_ids)}
    resp = binary_response_builder(success, message)
    return resp

"""
CRUD routes
"""
@app.route("/add_project", methods=["POST"])
def add_project():
    """
    This expects the object to be in snake case, not camelCase
    """
    json_request = request.get_json()
    print json_request
    data = json_request["data"]
    res = pc.create_project(data)
    message = {}
    message["project"] = res[1]
    resp = binary_response_builder(res, message)
    return resp

@app.route("/delete_project", methods=["POST"])
def delete_project():
    json_request = request.get_json()
    data = json_request["data"]
    project_id = data["project_id"]
    resp = binary_response_builder(pc.delete_project(project_id), {})
    return resp

@app.route("/update_project", methods=["POST"])
def update_project():
    """
    This expects the object to be in snake case, not camelCase
    """
    json_request = request.get_json()
    data = json_request["data"]
    project_id = data["project_id"]
    update_dict = data["update_dict"]
    resp = binary_response_builder(pc.update_project(project_id,
                                update_dict), {})
    return resp

@app.route("/get_project", methods=["POST"])
def get_project():
    json_request = request.get_json()
    data = json_request["data"]
    project_id = data["project_id"]
    message = {}
    project = pc.get_project(project_id)
    try:
        message["project"] = project.to_json()
        resp = binary_response_builder(success, message)
        return resp
    except:
        resp = binary_response_builder(fail, message)
        return resp

@app.route("/get_project_attribute", methods=["POST"])
def get_project_attribute():
    json_request = request.get_json()
    data = json_request["data"]
    project_id = data["project_id"]
    key = data["key"]
    attr = pc.get_simple_attribute(project_id, key)
    message = {"attr": attr}
    if attr is not None:
        resp = binary_response_builder(success, message)
    else:
        resp = binary_response_builder(fail, message)
    return resp
