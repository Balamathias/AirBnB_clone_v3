#!/usr/bin/python3
'''Contains the amenities view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """Retrieves the list of all Amenity objects"""
    all_objects = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in all_objects.values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def single_amenities(amenity_id):
    """Retrieves a Amenity object"""
    object_item = storage.get(Amenity, amenity_id)
    if not object_item:
        abort(404)
    return jsonify(object_item.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenities(amenity_id):
    """Returns an empty dictionary with the status code 200"""
    object_item = storage.get(Amenity, amenity_id)
    if not object_item:
        abort(404)

    object_item.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Returns the new Amenity with the status code 201"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if 'name' not in new_amenity:
        abort(400, "Missing name")

    object_item = Amenity(**new_amenity)
    storage.new(object_item)
    storage.save()
    return make_response(jsonify(object_item.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Returns the Amenity object with the status code 200"""
    object_item = storage.get(Amenity, amenity_id)
    if not object_item:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k not in ['id', 'created_at', 'update_at']:
            setattr(object_item, k, v)

    storage.save()
    return make_response(jsonify(object_item.to_dict()), 200)
