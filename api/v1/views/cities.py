#!/usr/bin/python3
""" Create the blueprint for City objects """
from flask import Blueprint, jsonify, abort, request
from models import storage
from models.city import City

app_views = Blueprint('cities', __name__, url_prefix='/api/v1')


@app_views.route("/", methods=["GET"], strict_slashes=False)
def cities():
    """ Retrieves the list of all City objects """
    all_cities = [city.to_dict() for city in storage.all("City").values()]
    return jsonify(all_cities)


@app_views.route("/<city_id>", methods=["GET"], strict_slashes=False)
def city(city_id):
    """ Retrieves a City object """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/", methods=["POST"], strict_slashes=False)
def add_city():
    """ Creates a new City """
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400
    if data is None:
        return "Not a JSON", 400
    if 'name' not in data:
        return "Missing name", 400
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400
    if data is None:
        return "Not a JSON", 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

