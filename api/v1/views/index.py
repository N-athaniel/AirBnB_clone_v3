#!/usr/bin/python3
"""A script that retrieves the number of each objects by type"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User,
}


@app_views.route("/status", strict_slashes=False)
def status():
    """Status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Retrieve the number of each objects by type"""
    statistics = {}

    for key, value in classes.items():
        statistics[key] = storage.count(value)

    return jsonify(statistics)
