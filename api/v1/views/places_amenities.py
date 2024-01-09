#!/usr/bin/python3
"""
flask RESTful API
    GET /api/v1/places/<place_id>/amenities
    DELETE /api/v1//places/<place_id>/amenities/<amenity_id>
    POST /places/<place_id>/amenities/<amenity_id>
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from os import environ
from models import storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def get_amenities_(place_id):
    """
    Retrieves the list of all amenity objects of a Place.
    """
    am = []
    pl = storage.get("Place", place_id)
    if not pl:
        abort(404)
    for r in pl.amenities:
        if environ.get('HBNB_TYPE_STORAGE') == "db":
            am.append(r.to_dict())
    for r in pl.amenity_ids:
        if environ.get('HBNB_TYPE_STORAGE') != "db":
            am.append(storage.get("Amenity", r).to_dict())
    return jsonify(am)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place:
    DELETE /api/v1/places/<place_id>/amenities/<amenity_id>
    """
    pl = storage.get("Place", place_id)
    am = storage.get("Amenity", amenity_id)
    if not pl:
        abort(404)
    if not am:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') != "db":
        if amenity_id not in pl.amenity_ids:
            abort(404)
        pl.amenity_ids.remove(amenity_id)
    else:
        if am not in pl.amenities:
            abort(404)
        pl.amenities.remove(am)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def post_amenity_(place_id, amenity_id):
    """
    Creates a amenity.
    """
    data = request.get_json()
    pl = storage.get("Place", place_id)
    am = storage.get("Amenity", amenity_id)
    if not pl:
        abort(404)
    if not am:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') != "db":
        if amenity_id in pl.amenity_ids:
            return make_response(jsonify(am.to_dict()), 200)
        else:
            pl.amenity_ids.append(amenity_id)
    else:
        if am in pl.amenities:
            return make_response(jsonify(am.to_dict()), 200)
        else:
            pl.amenities.append(am)
    storage.save()
    return make_response(jsonify(am.to_dict()), 201)
