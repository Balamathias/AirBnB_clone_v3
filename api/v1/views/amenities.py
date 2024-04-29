#!/usr/bin/python3
"""
route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    retrieves all Amenity objects
    :return: json of all states
    """
    am_list = []
    am_obj = storage.all("Amenity")
    for obj in am_obj.values():
        am_list.append(obj.to_json())

    return jsonify(am_list)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    create amenity route
    :return: newly created amenity obj
    """
    amenity_to_json = request.get_json(silent=True)
    if amenity_to_json is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_to_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_to_json)
    new_amenity.save()
    resp = jsonify(new_amenity.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    gets a specific Amenity object by ID
    :param amenity_id: amenity object id
    :return: state obj with the specified id or error
    """

    received_object = storage.get("Amenity", str(amenity_id))

    if received_object is None:
        abort(404)

    return jsonify(received_object.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """
    updates specific Amenity object by ID
    :param amenity_id: amenity object ID
    :return: amenity object and 200 on success, or 400 or 404 on failure
    """
    amenity_to_json = request.get_json(silent=True)
    if amenity_to_json is None:
        abort(400, 'Not a JSON')
    received_object = storage.get("Amenity", str(amenity_id))
    if received_object is None:
        abort(404)
    for key, val in amenity_to_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(received_object, key, val)
    received_object.save()
    return jsonify(received_object.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    deletes Amenity by id
    :param amenity_id: Amenity object id
    :return: empty dict with 200 or 404 if not found
    """

    received_object = storage.get("Amenity", str(amenity_id))

    if received_object is None:
        abort(404)

    storage.delete(received_object)
    storage.save()

    return jsonify({})
