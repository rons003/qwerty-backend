from app import app, db
from flask import render_template, redirect, url_for, request, jsonify, abort, session
# import app.controllers.badge_controller as bc
import app.controllers.group_controller as gc
import app.controllers.challenge_controller as cc
import app.controllers.user_controller as uc
import app.controllers.chapter_item_controller as cic
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
CRUD routes
"""


@app.route("/get_all_chapter_item/<int:offset>/<int:size>", methods=["GET"])
def get_all_chapter_item(offset, size):
    chapter_item = cic.get_all_chapter_item(offset, size)
    message = {"data": chapter_item}
    resp = binary_response_builder(success, message)
    return resp


@app.route("/create_chapter_item", methods=["POST"])
def create_chapter_item():
    json_request = request.get_json()
    data = json_request["data"]
    resp = binary_response_builder(
        cic.create_chapter_item(data), {})
    return resp


@app.route("/delete_chapter_item", methods=["POST"])
def delete_chapter_item():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_item_id = data["chapter_item_id"]
    resp = binary_response_builder(
        cic.delete_chapter_item(chapter_item_id), {})
    return resp


@app.route("/get_chapter_item", methods=["POST"])
def get_chapter_item():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_item_id = data["chapter_item_id"]
    message = {}
    chapter_item = cic.get_chapter_item(chapter_item_id)
    try:
        message["data"] = chapter_item.to_json()
        resp = binary_response_builder(success, message)
        return resp
    except:
        resp = binary_response_builder(fail, message)
        return resp


@app.route("/update_chapter_item", methods=["POST"])
def update_chapter_item():
    json_request = request.get_json()
    data = json_request["data"]
    chapter_item_id = data["chapter_item_id"]
    update_dict = data["update_dict"]
    resp = binary_response_builder(cic.update_chapter_item(chapter_item_id,
                                                           update_dict), {})
    return resp

@app.route("/get_chapter_item_from_chapter", methods=["POST"])
def get_chapter_item_from_chapter():
    json_request = request.get_json()
    data = json_request["data"]
    chapter = chc.get_chapter_using_id(data["chapter_id"])
    chapter_item_data = []
    for ci_id in chapter.chapter_items:
        chapter_item_data.append(cic.get_chapter_item(ci_id))
    message  = { "data": chapter_item_data }
    resp = binary_response_builder(success, message)
    return resp
