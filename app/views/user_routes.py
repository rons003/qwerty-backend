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

@app.route("/get_users_from_school", methods=["POST"])
def get_users_from_school():
    json_request = request.get_json()
    data = json_request["data"]
    school_name = data["school_name"]
    res = {"usernames": uc.get_users_from_school(school_name)}
    resp = binary_response_builder(success, res)
    return resp

@app.route("/get_users_students", methods=["POST"])
def get_users_students():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    res = {"users": uc.get_users_students(user_id)}
    resp = binary_response_builder(success, res)
    return resp


"""
CRUD routes
"""
@app.route("/add_user", methods=["POST"])
def add_user():
    json_request = request.get_json()
    print json_request
    data = json_request["data"]
    resp = binary_response_builder(uc.create_user(data), {})
    return resp

@app.route("/delete_user", methods=["POST"])
def delete_user():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    resp = binary_response_builder(uc.delete_user(user_id), {})
    return resp

@app.route("/update_user", methods=["POST"])
def update_user():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    update_dict = data["update_dict"]
    resp = binary_response_builder(uc.update_user(user_id,
                                update_dict), {})
    return resp


@app.route("/update_user_account", methods=["POST"])
def update_user_account():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    update_dict = data["update_dict"]
    update_dict['pwd'] = uc.hash_password(update_dict['pwd'])
    resp = binary_response_builder(uc.update_user(user_id,
                                                  update_dict), {})
    return resp

@app.route("/update_password", methods=["POST"])
def update_password():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    old_password = data["old_password"]
    new_password = data["new_password"]
    success = uc.update_user_password(user_id, old_password, new_password)
    resp = binary_response_builder(success, {})
    return resp

@app.route("/reset_password", methods=["POST"])
def reset_password():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    new_password = data["new_password"]
    success = uc.reset_password(user_id, new_password)
    resp = binary_response_builder(success, {})
    return resp

@app.route("/get_user", methods=["POST"])
def get_user():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    message = {}
    user = uc.get_user(user_id)
    try:
        message["user"] = user.to_json()
        resp = binary_response_builder(success, message)
        return resp
    except:
        resp = binary_response_builder(fail, message)
        return resp

@app.route("/get_user_attribute", methods=["POST"])
def get_user_attribute():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    key = data["key"]
    attr = uc.get_simple_attribute(user_id, key)
    message = {"attr": attr}
    if attr is not None:
        resp = binary_response_builder(success, message)
    else:
        resp = binary_response_builder(fail, message)
    return resp

@app.route("/get_all_usernames/<int:usertype>", methods=["GET"])
def get_all_usernames(usertype):
    """
    Gets usernames of a specified type.
    Args:
        usertype    : int
        0 - students
        1 - parents
        2 - teachers
        3 - all usernames
    """
    usernames = uc.get_all_usernames(usertype)
    message = {"data": usernames}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/get_all_users/<int:offset>/<int:size>", methods=["GET"])
def get_all_users(offset,size):
    users = uc.get_all_users(offset,size)
    message = {"data": users}
    resp = binary_response_builder(success, message)
    return resp    

@app.route("/get_all_students/<int:offset>/<int:size>", methods=["GET"])
def get_all_students(offset,size):
    users = uc.get_all_students(offset,size)
    message = {"data": users}
    resp = binary_response_builder(success, message)
    return resp  

@app.route("/get_user_groups", methods=["POST"])
def get_user_groups():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    groups = uc.get_simple_attribute(user_id, "groups")
    message = {"groups": groups}
    if groups is not None:
        resp = binary_response_builder(success, message)
    else:
        resp = binary_response_builder(fail, message)
    return resp

@app.route("/search_user/<search>/<usertype>", methods=["GET"])
def search_user(search,usertype):
    users = uc.search_user(search,usertype)
    message = {"data": users}
    resp = binary_response_builder(success, message)
    return resp

@app.route("/search_usertype/<search_usertype>", methods=["GET"])
def search_usertype(search_usertype):
    users = uc.search_usertype(search_usertype)
    message = {"data": users}
    resp = binary_response_builder(success, message)
    return resp

@app.route("/get_teacher_using_school", methods=["POST"])
def get_teacher_using_school():
    json_request = request.get_json()
    data = json_request["data"]
    school_id = data["school_id"]
    teachers = uc.get_teacher_using_school(school_id)
    message = {}
    message["data"] = teachers
    resp = binary_response_builder(success,message)
    return resp