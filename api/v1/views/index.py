#!/usr/bin/python3
""" Index file of flask app """
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status")
def status():
    """ Status of the api """
    stat = {
            "status": "OK"
            }
    return jsonify(stat)


@app_views.route("/stats")
def stats():
    """ Returns number of each object by type """
    classes = {"User": "users",
                "Amenity": "amenities", "City": "cities",
                "Place": "places", "Review": "reviews",
                "State": "states"}
    numbers = {}
    for key, val in classes.items():
        numbers[val] = storage.count(key)
    return jsonify(numbers)
