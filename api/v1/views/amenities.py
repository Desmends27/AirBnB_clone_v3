#!/usr/bin/python3
""" Create the blueprint for Amenity objects """
from flask import Blueprint, jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities():
    """ Retrieves the list of all Amenity objects """
    all_amenities = [amenity.to_dict() for amenity in storage.all("Amenity").values()]
    return jsonify(all_amenities)


@app_views.route("/amenities/<int: amenity_id>", methods=["GET"], strict_slashes=False)
def amenity(amenity_id):
    """ Retrieves a Amenity object """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<int:amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def add_amenity():
    """ Creates a new Amenity """
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400
    if data is None:
        return "Not a JSON", 400
    if 'name' not in data:
        return "Missing name", 400
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<int:amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a Amenity object """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400
    if data is None:
        return "Not a JSON", 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
