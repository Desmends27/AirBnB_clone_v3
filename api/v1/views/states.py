#!/usr/bin/python3
""" Create the blueprint """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from flask import abort, request

@app_views.route("/states/", methods=["GET"])
def states():
    """ Retireves a list of State objects """
    all_states = [state.to_json() for state in storage.all("State").values()]
    return jsonify(all_states)


@app_views.route("/states/<int:state_id>", methods=["GET"])
def state(state_id=None):
    """ Retrives a particular state object """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_json())

@app_views.route("/states/<int:state_id>", methods=["DELETE"])
def delete_state(state_id=None):
    """ Deletes a particular state object """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200

@app_views.route("/states", methods=["POST"])
def add_state():
    """ Adds a new state """
    response = None
    try:
        response = request.get_json()
    except:
        response = None
    if response is None:
        return "Not a JSON", 400
    if 'name' not in response.keys():
        return "Missing name", 400
    s = State(**r)
    s.save()
    return jsonify(s.to_json()), 201

@app_views.route("/states/<int:state_id>", methods=["PUT"])
def update_state(state_id):
    response = None
    try: 
        reponse = request.get_json()
    except:
        response = None
    if response is None:
        return "Not a JSON", 400
    if 'name' not in response.keys():
        return "Missing name", 400
    s = storage.get("State", state_id)
    if state is None:
        abort(404)
    for k in ("id", "create_at", "update_at"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(state, k, v)
    state.save()
    return jsonify(state.to_json()), 200
