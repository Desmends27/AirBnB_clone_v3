#!/usr/bin/python3
""" Index file of flask app """
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """ Status of the api """
    stat = {
            "status": "OK"
            }
    return jsonify(stat)
