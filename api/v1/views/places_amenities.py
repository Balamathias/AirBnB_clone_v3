#!/usr/bin/python3
'''Contains the places_amenities view for the API.'''
from flask import abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models import amenity
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place_object = storage.get(Place, place_id)
    if not place_object:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        obj = [amenity.to_dict() for amenity in place_object.amenities]
    else:
        obj = [storage.get(Amenity, amenity_id).to_dict()
               for amenity_id in place_object.amenity_ids]
    return jsonify(obj)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
    """Returns an empty dictionary with the status code 200"""
    place_object = storage.get(Place, place_id)
    if not place_object:
        abort(404)

    amenity_object = storage.get(Amenity, amenity_id)
    if not amenity_object:
        abort(404)

    for elem in place_object.amenities:
        if elem.id == amenity_object.id:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                place_object.amenities.remove(amenity_object)
            else:
                place_object.amenity_ids.remove(amenity_object)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Returns the Amenity with the status code 201"""
    place_object = storage.get(Place, place_id)
    if not place_object:
        abort(404)

    amenity_object = storage.get(Amenity, amenity_id)
    if not amenity_object:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity_object in place_object.amenities:
            return make_response(jsonify(amenity_object.to_dict()), 200)
        place_object.amenities.append(amenity_object)
    else:
        if amenity_id in place_object.amenity_ids:
            return make_response(jsonify(amenity_object.to_dict()), 200)
        place_object.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity_object.to_dict()), 201)
