from app import app, db
from flask import render_template, redirect, url_for, request, jsonify, abort, session
# import app.controllers.badge_controller as bc
import app.controllers.group_controller as gc
import app.controllers.chapter_controller as cc
import app.controllers.user_controller as uc
import app.controllers.chapter_controller as chc
import app.controllers.chapter_item_controller as cic
import app.controllers.module_controller as moc
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

@app.route("/add_chapter_item_to_chapter", methods=["POST"])
def add_chapter_item_to_chapter():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_item_id = data["chapter_item_id"]
    chapter_id = data["chapter_id"]
    resp = binary_response_builder(
        chc.add_chapter_item_to_chapter(chapter_item_id, chapter_id), {})
    return resp


@app.route("/delete_chapter_item_from_chapter", methods=["POST"])
def delete_chapter_item_from_chapter():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_item_id = data["chapter_item_id"]
    chapter_id = data["chapter_id"]
    resp = binary_response_builder(
        chc.delete_chapter_item_from_chapter(chapter_item_id, chapter_id), {})
    return resp


@app.route("/add_challenge_to_chapter", methods=["POST"])
def add_challenge_to_chapter():
    json_request = request.get_json()
    data = json_request["data"]
    challenge_id = data["challenge_id"]
    chapter_id = data["chapter_id"]
    resp = binary_response_builder(
        chc.add_challenge(challenge_id, chapter_id), {})
    return resp


@app.route("/delete_challenge_from_chapter", methods=["POST"])
def delete_challenge_from_chapter():
    json_request = request.get_json()
    data = json_request["data"]
    challenge_id = data["challenge_id"]
    chapter_id = data["chapter_id"]
    resp = binary_response_builder(
        chc.delete_challenge(challenge_id, chapter_id), {})
    return resp


@app.route("/get_challenge_from_chapter", methods=["POST"])
def get_challenge_from_chapter():
    json_request = request.get_json()
    data = json_request["data"]
    challenge_id = data["challenge_id"]
    chapter_id = data["chapter_id"]
    challenge = chc.get_challenge(challenge_id, chapter_id)
    message = {"challenge": challenge.to_json()}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/get_challenges_from_chapter", methods=["POST"])
def get_challenges_from_chapter():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_id = data["chapter_id"]
    challenges = chc.get_chapter_challenges(chapter_id)
    message = {"challenges": challenges}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/complete_challenge", methods=["POST"])
def complete_challenge():
    json_request = request.get_json()
    data = json_request["data"]
    challenge_id = data["challenge_id"]
    chapter_id = data["chapter_id"]
    resp = binary_response_builder(
        chc.complete_challenge(challenge_id, chapter_id), {})
    return resp


@app.route("/uncomplete_challenge", methods=["POST"])
def uncomplete_challenge():
    json_request = request.get_json()
    data = json_request["data"]
    challenge_id = data["challenge_id"]
    chapter_id = data["chapter_id"]
    resp = binary_response_builder(
        chc.uncomplete_challenge(challenge_id, chapter_id), {})
    return resp


"""
CRUD routes
"""


@app.route("/get_all_chapter/<int:offset>/<int:size>", methods=["GET"])
def get_all_chapter(offset, size):
    chapter = chc.get_all_chapter(offset, size)
    message = {"data": chapter}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/create_chapter", methods=["POST"])
def create_chapter():
    json_request = request.get_json()
    data = json_request["data"]
    resp = binary_response_builder(chc.create_chapter(data), {})
    return resp


@app.route("/delete_chapter", methods=["POST"])
def delete_chapter():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_ids = data["chapter_id"]
    for chapter_id in chapter_ids:
        chc.delete_chapter(chapter_id)
    resp = binary_response_builder(success, {})
    return resp


@app.route("/get_chapter", methods=["POST"])
def get_chapter():
    json_request = request.get_json()
    data = json_request["data"]
    module_id = data["module_id"]
    chapter = chc.get_chapter_using_school(module_id)
    message = {"data": chapter}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/get_chapters_in_json", methods=["POST"])
def get_chapters_in_json():
    json_request = request.get_json()
    data = json_request["data"]
    message = {"chapters": chc.get_chapters_in_json()}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/update_chapter", methods=["POST"])
def update_chapter():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_id = data["chapter_id"]
    update_dict = data["update_dict"]
    resp = binary_response_builder(chc.update_chapter(chapter_id,
                                                      update_dict), {})
    return resp


@app.route("/get_chapter_item_objects_list", methods=["POST"])
def get_chapter_item_objects_list():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_id = data["chapter_id"]
    chapter = chc.get_chapter(chapter_id)
    chapter_items = cic.get_chapter_item_objects_list(chapter.chapter_items)
    message = {"chapter_items": chapter_items}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/get_chapter_attribute", methods=["POST"])
def get_chapter_attribute():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_id = data["chapter_id"]
    key = data["key"]
    attr = chc.get_simple_attribute(chapter_id, key)
    message = {"attr": attr}
    if attr is not None:
        resp = binary_response_builder(success, message)
    else:
        resp = binary_response_builder(fail, message)
    return resp
