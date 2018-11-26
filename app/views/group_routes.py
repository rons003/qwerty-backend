from app import app, db
from flask import render_template, redirect, url_for, request, jsonify, abort, session
# import app.controllers.badge_controller as bc
import app.controllers.group_controller as gc
import app.controllers.challenge_controller as cc
import app.controllers.user_controller as uc
import app.controllers.chapter_controller as chc
from app.models.templates import *
import os, json
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

"""
Group routes
"""
@app.route("/add_chapter_to_group", methods=["POST"])
def add_chapter_to_group():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_id = data["chapter_id"]
    group_id = data["group_id"]
    resp = binary_response_builder(gc.add_chapter(chapter_id, group_id), {})
    return resp

@app.route("/delete_chapter_from_group", methods=["POST"])
def delete_chapter_from_group():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_id = data["chapter_id"]
    group_id = data["group_id"]
    resp = binary_response_builder(gc.delete_chapter(chapter_id, group_id), {})
    return resp

@app.route("/get_chapter_from_group", methods=["POST"])
def get_chapter_from_group():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_id = data["chapter_id"]
    group_id = data["group_id"]
    chapter = gc.get_chapter(chapter_id, group_id)
    message = {"chapter": chapter.to_json()}
    resp = binary_response_builder(success, message)
    return resp

@app.route("/add_user_to_group", methods=["POST"])
def add_user_to_group():
    json_request = request.get_json()
    data = json_request["data"]
    to_be_added_id = data["to_be_added_id"]
    adder_id = data["adder_id"]
    group_id = data["group_id"]

    uc.add_user_to_group(adder_id, to_be_added_id, group_id)
    list_type = int(data["list_type"])
    resp = binary_response_builder(gc.add_user(to_be_added_id,
                        group_id, list_type), {})
    return resp

@app.route("/delete_user_from_group", methods=["POST"])
def delete_user_from_group():
    json_request = request.get_json()
    data = json_request["data"]
    to_be_deleted_id = data["to_be_deleted_id"]
    deleter_id = data["deleter_id"]
    group_id = data["group_id"]

    uc.delete_user_from_group(deleter_id, to_be_deleted_id, group_id)
    list_type = int(data["list_type"])
    resp = binary_response_builder(gc.delete_user(to_be_deleted_id,
                    group_id, list_type), {})
    return resp

@app.route("/get_user_from_group", methods=["POST"])
def get_user_from_group():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    group_id = data["group_id"]
    list_type = int(data["list_type"])
    message = {}
    res = gc.get_user(user_id, group_id, list_type)
    message["user"] = res[1].to_json()
    if res[0]:
        resp = binary_response_builder(success, message)
    else:
        resp = binary_response_builder(fail, message)
    return resp

@app.route("/activate_user_in_group", methods=["POST"])
def activate_user_in_group():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    group_id = data["group_id"]
    resp = binary_response_builder(gc.activate_user(user_id,
                            group_id), {})
    return resp

@app.route("/deactivate_user_in_group", methods=["POST"])
def deactivate_user_in_group():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    group_id = data["group_id"]
    resp = binary_response_builder(gc.deactivate_user(user_id,
                            group_id), {})
    return resp

"""
CRUD routes
"""
@app.route("/create_group", methods=["POST"])
def create_group():
    json_request = request.get_json()
    data = json_request["data"]
    group_dict  = data["group_dict"]
    creator = data["creator_id"]
    res = gc.create_group(group_dict)
    group = res[1]
    uc.add_group(creator, group.id)
    resp = binary_response_builder(res, {})
    return resp

@app.route("/delete_group", methods=["POST"])
def delete_group():
    json_request = request.get_json()
    data = json_request["data"]
    group_id = data["group_id"]
    resp = binary_response_builder(gc.delete_group(group_id), {})
    return resp

@app.route("/get_group", methods=["POST"])
def get_group():
    json_request = request.get_json()
    data = json_request["data"]
    group_id = data["group_id"]
    message = {}
    group = gc.get_group(group_id)
    try:
        message["group"] = group.to_json()
        resp = binary_response_builder(success, message)
        return resp
    except:
        resp = binary_response_builder(fail, message)
        return resp

@app.route("/update_group", methods=["POST"])
def update_group():
    json_request = request.get_json()
    data = json_request["data"]
    group_id = data["group_id"]
    update_dict = data["update_dict"]
    resp = binary_response_builder(gc.update_group(group_id,
                                update_dict), {})
    return resp

@app.route("/get_users_from_group", methods=["POST"])
def get_users_from_group():
    json_request = request.get_json()
    data = json_request["data"]
    group_id = data["group_id"]
    message = {}
    users = gc.get_users(group_id)
    message["users"] = users
    resp = binary_response_builder(success, message)
    # if len(users) != 0:
    #     resp = binary_response_builder(success, message)
    # else:
    #     resp = binary_response_builder(fail, message)
    return resp

@app.route("/get_emails_from_group", methods=["POST"])
def get_emails_from_group():
    json_request = request.get_json()
    data = json_request["data"]
    group_id = data["group_id"]
    message = {}
    emails = gc.get_emails(group_id)
    message["emails"] = emails
    resp = binary_response_builder(success, message)
    return resp

@app.route("/get_group_attribute", methods=["POST"])
def get_group_attribute():
    json_request = request.get_json()
    data = json_request["data"]
    group_id = data["group_id"]
    key = data["key"]
    attr = gc.get_simple_attribute(group_id, key)
    message = {"attr": attr}
    if attr is not None:
        resp = binary_response_builder(success, message)
    else:
        resp = binary_response_builder(fail, message)
    return resp

@app.route("/add_assignment_to_group", methods=["POST"])
def add_assignment_to_group():
    json_request = request.get_json()
    data = json_request["data"]
    group_id = data["group_id"]
    assignment_dict = data["assignment_dict"]
    resp = binary_response_builder(gc.add_assignment_to_group(group_id, assignment_dict), {})
    return resp

@app.route("/remove_assignment_from_group", methods=["POST"])
def remove_assignment_from_group():
    json_request = request.get_json()
    data = json_request["data"]
    group_id = data["group_id"]
    assignment_id = data["assignment_id"]
    resp = binary_response_builder(gc.remove_assignment_from_group(group_id, assignment_id), {})
    return resp

@app.route("/get_user_objects_list", methods=["POST"])
def get_user_objects_list():
    json_request = request.get_json()
    data = json_request["data"]
    group_id = data["group_id"]
    user_type = data["user_type"]
    group = gc.get_group(group_id)

    if user_type == 0:
        user_objects = uc.get_user_objects_list(group.students)
    else:
        user_objects = uc.get_user_objects_list(group.admins)
    message = {"data": user_objects}
    resp = binary_response_builder(success, message)
    return resp

@app.route("/get_chapter_objects_list", methods=["POST"])
def get_chapter_objects_list():
    json_request = request.get_json()
    data = json_request["data"]
    group_id = data["group_id"]
    chapter_objects = gc.get_chapter_objects_list(group_id)
    message = {"data": chapter_objects}
    resp = binary_response_builder(success, message)
    return resp

# @app.route("/get_challenge_objects_list", methods=["POST"])
# def get_challenge_objects_list():
#     json_request = request.get_json()
#     data = json_request["data"]
#     group_id = data["group_id"]
#     challenge_objects = gc.get_challenge_objects_list(group_id)
#     message = {"data": challenge_objects}
#     resp = binary_response_builder(success, message)
#     return resp

@app.route("/get_assignment_objects_list", methods=["POST"])
def get_assignment_objects_list():
    json_request = request.get_json()
    data = json_request["data"]
    group_id = data["group_id"]
    assignment_objects = gc.get_assignment_objects_list(group_id)
    message = {"data": assignment_objects}
    resp = binary_response_builder(success, message)
    return resp
