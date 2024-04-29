#!/usr/bin/python3
'''Contains the index view for the API.'''
from flask import jsonify
from api.v1.views import app_views
from models import storage as store


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns JSON """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat():
    """returns the number of each objects by type"""
    return jsonify(
        amenities=store.count('Amenity'),
        cities=store.count('City'),
        places=store.count('Place'),
        reviews=store.count('Review'),
        states=store.count('State'),
        users=store.count('User')
    )
