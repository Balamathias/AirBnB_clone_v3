#!/usr/bin/python3
'''Contains the places_reviews view for the API.'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place_object_item = storage.get(Place, place_id)
    if not place_object_item:
        abort(404)
    return jsonify([obj.to_dict() for obj in place_object_item.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def single_review(review_id):
    """Retrieves a Review object"""
    object_item = storage.get(Review, review_id)
    if not object_item:
        abort(404)
    return jsonify(object_item.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """Returns an empty dictionary with the status code 200"""
    object_item = storage.get(Review, review_id)
    if not object_item:
        abort(404)
    object_item.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def push_review(place_id):
    """Returns the new Review with the status code 201"""
    place_object_item = storage.get(Place, place_id)
    if not place_object_item:
        abort(404)

    new_review = request.get_json()
    if not new_review:
        abort(400, "Not a JSON")
    if 'user_id' not in new_review:
        abort(400, "Missing user_id")
    user_id = new_review['user_id']
    user_object = storage.get(User, user_id)
    if not user_object:
        abort(404)
    if 'text' not in new_review:
        abort(400, "Missing text")

    obj = Review(**new_review)
    setattr(obj, 'place_id', place_id)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Returns the Review object with the status code 200"""
    object_item = storage.get(Review, review_id)
    if not object_item:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(object_item, k, v)

    storage.save()
    return make_response(jsonify(object_item.to_dict()), 200)
