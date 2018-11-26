from app import app, db
from flask import render_template, redirect, url_for, request, jsonify, abort, session
# # import app.controllers.badge_controller as bc
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

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/signin", methods=["POST"])
def signin():
    json_request = request.get_json()
    data = json_request["data"]
    username = data["username"]
    username = username.lower()
    pwd = data["pwd"]
    token = uc.login(username, pwd)
    if token is not None:
        user = uc.get_user_by_username(username)
        message = {"username": username, "user": user, "token": token}
        resp = binary_response_builder(success, message)
    else:
        resp = binary_response_builder(fail, {})
    return resp
