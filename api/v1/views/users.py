#!/usr/bin/python3
""" Create the blueprint for User objects """
from flask import Blueprint, jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/", methods=["GET"], strict_slashes=False)
def users():
    """ Retrieves the list of all User objects """
    all_users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(all_users)


@app_views.route("/<user_id>", methods=["GET"], strict_slashes=False)
def user(user_id):
    """ Retrieves a User object """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/", methods=["POST"], strict_slashes=False)
def add_user():
    """ Creates a new User """
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400
    if data is None:
        return "Not a JSON", 400
    if 'email' not in data:
        return "Missing email", 400
    if 'password' not in data:
        return "Missing password", 400
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400
    if data is None:
        return "Not a JSON", 400
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
