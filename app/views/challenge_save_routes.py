from app import app, db
from flask import render_template, redirect, url_for, request, jsonify, abort, session
from app.models.templates import *
import app.controllers.challenge_save_controller as csc
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

@app.route("/get_challenge_save_for_user_and_challenge", methods=["POST"])
def get_challenge_save_for_user_and_challenge():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    challenge_id = data["challenge_id"]
    message = {"challenge_save": csc.get_challenge_save_for_user_and_challenge(user_id, challenge_id)}
    resp = binary_response_builder(success, message)
    return resp

@app.route("/set_challenge_save_for_user_and_challenge", methods=["POST"])
def set_challenge_save_for_user_and_challenge():
    json_request = request.get_json()
    data = json_request["data"]
    user_id = data["user_id"]
    challenge_id = data["challenge_id"]
    update_dict = data["update_dict"]
    resp = binary_response_builder(csc.set_challenge_save_for_user_and_challenge(user_id=user_id,
                            challenge_id=challenge_id, update_dict=update_dict), {})
    return resp
