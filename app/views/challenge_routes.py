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
Challenge routes
"""
@app.route("/assign_challenge", methods=["POST"])
def assign_challenge():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    group_id = data["group_id"]
    challenge_id = data["challenge_id"]
    points = data["points"]
    due_date = data["due_date"]
    resp = binary_response_builder(uc.assign_challenge(user_id, group_id,
                            challenge_id, points, due_date), {})

@app.route("/create_challenge", methods=["POST"])
def create_challenge():
    json_request = request.get_json()
    data = json_request["data"]
    resp = binary_response_builder(cc.create_challenge(data), {})
    return resp

@app.route("/delete_challenge", methods=["POST"])
def delete_challenge():
    json_request = request.get_json()
    data = json_request["data"]
    challenge_id = data["challenge_id"]
    resp = binary_response_builder(cc.delete_challenge(challenge_id), {})
    return resp

@app.route("/get_challenge", methods=["POST"])
def get_challenge():
    json_request = request.get_json()
    data = json_request["data"]
    challenge_id = data["challenge_id"]
    message = {}
    challenge = cc.get_challenge(challenge_id)
    try:
        message["challenge"] = challenge.to_json()
        resp = binary_response_builder(success, message)
        return resp
    except:
        resp = binary_response_builder(fail, message)
        return resp

@app.route("/get_challenges", methods=["POST"])
def get_challenges():
    json_request = request.get_json()
    data = json_request["data"]
    message = {"challenges": cc.get_challenges()}
    resp = binary_response_builder(success, message)
    return resp

@app.route("/update_challenge", methods=["POST"])
def update_challenge():
    json_request = request.get_json()
    data = json_request["data"]
    challenge_id = data["challenge_id"]
    update_dict = data["update_dict"]
    resp = binary_response_builder(cc.update_challenge(challenge_id,
                                update_dict), {})
    return resp

@app.route("/get_challenge_attribute", methods=["POST"])
def get_challenge_attribute():
    json_request = request.get_json()
    data = json_request["data"]
    challenge_id = data["challenge_id"]
    key = data["key"]
    attr = cc.get_simple_attribute(challenge_id, key)
    message = {"attr": attr}
    if attr is not None:
        resp = binary_response_builder(success, message)
    else:
        resp = binary_response_builder(fail, message)
    return resp
