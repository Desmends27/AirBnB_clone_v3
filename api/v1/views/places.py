#!/usr/bin/python3
""" Create the blueprint for Place objects """
from flask import Blueprint, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User

app_views = Blueprint('places', __name__, url_prefix='/api/v1')


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def city_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place(place_id):
    """ Retrieves a Place object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def add_place(city_id):
    """ Creates a new Place """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400
    if data is None:
        return "Not a JSON", 400
    if 'user_id' not in data:
        return "Missing user_id", 400
    if 'name' not in data:
        return "Missing name", 400
    user_id = data.get('user_id')
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    new_place = Place(city_id=city_id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400
    if data is None:
        return "Not a JSON", 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id',
                       'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
