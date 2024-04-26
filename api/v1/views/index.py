from flask import jsonify, request
from models import storage
from api.v1.views import app_views

#!/usr/bin/python3
"""
Flask route that returns json status response
"""


@app_views.route('/status', methods=['GET'])
def status():
    """
    Function for status route that returns the status
    """
    if request.method == 'GET':
        banana_response = {"status": "OK"}
        return jsonify(banana_response)


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Function to return the count of all class objects
    """
    if request.method == 'GET':
        response = {}
        PLURALS = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in PLURALS.items():
            response[value] = storage.count(key)
        return jsonify(response)
