#!/usr/bin/python3
"""
route for handling State objects and operations
"""

from flask import jsonify, abort, request

from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    retrieves all State objects
    :return: json of all states
    """
    states = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        states.append(obj.to_json())

    return jsonify(states)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    create state route
    :return: newly created state obj
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    resp = jsonify(new_state.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    gets a specific State object by ID
    :param state_id: state object id
    :return: state obj with the specified id or error
    """

    received_object = storage.get("State", str(state_id))

    if received_object is None:
        abort(404)

    return jsonify(received_object.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    updates specific State object by ID
    :param state_id: state object ID
    :return: state object and 200 on success, or 400 or 404 on failure
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    received_object = storage.get("State", str(state_id))
    if received_object is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(received_object, key, val)
    received_object.save()
    return jsonify(received_object.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    deletes State by id
    :param state_id: state object id
    :return: empty dict with 200 or 404 if not found
    """

    received_object = storage.get("State", str(state_id))

    if received_object is None:
        abort(404)

    storage.delete(received_object)
    storage.save()

    return jsonify({})
