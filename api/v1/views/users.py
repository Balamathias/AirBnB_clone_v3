#!/usr/bin/python3
'''Contains the users view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Retrieves the list of all User objects"""
    users = storage.all(User)
    return jsonify([user_obj.to_dict() for user_obj in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def single_user(user_id):
    """Retrieves a User object"""
    object_item = storage.get(User, user_id)
    if not object_item:
        abort(404)
    return jsonify(object_item.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """Returns an empty dictionary with the status code 200"""
    object_item = storage.get(User, user_id)
    if not object_item:
        abort(404)
    object_item.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Returns the new User with the status code 201"""
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if 'email' not in new_user:
        abort(400, "Missing email")
    if 'password' not in new_user:
        abort(400, 'Missing password')

    object_item = User(**new_user)
    storage.new(object_item)
    storage.save()
    return make_response(jsonify(object_item.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Returns the User object with the status code 200"""
    object_item = storage.get(User, user_id)
    if not object_item:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(object_item, k, v)

    storage.save()
    return make_response(jsonify(object_item.to_dict()), 200)
