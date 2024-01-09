#!/usr/bin/python3
"""
flask RESTful API
    GET /api/v1/cities/<city_id>/places
    GET /api/v1/places/<place_id>
    DELETE /api/v1/places/<place_id>
    POST /api/v1/cities/<city_id>/places
    PUT /api/v1/places/<place_id>
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City.
    If the city_id is not linked to any City object,
        raise a 404 error
    """
    pl = []
    ct = storage.get("City", city_id)
    if not ct:
        abort(404)
    for place in ct.places:
        pl.append(place.to_dict())
    return jsonify(pl)


@app_views.route("/places/<place_id>/",
                 methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object by id. If the place_id is not
    linked to any Place object, raise a 404 error.
    """
    pl = storage.get("Place", place_id)
    if not pl:
        abort(404)
    return jsonify(pl.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object. If the place_id is not
    linked to any Place object, raise a 404 error.
    Returns an empty dictionary with the status code 200.
    """
    pl = storage.get("Place", place_id)
    if not pl:
        abort(404)
    pl.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """
    Creates a Place.
    f the city_id is not linked to any City object,
        raise a 404 error.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    If the dictionary doesn’t contain the key name,
        raise a 400 error with the message Missing name
    Returns the new Place with the status code 201.
    """
    data = request.get_json()
    ct = storage.get("City", city_id)
    if not ct:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    u = storage.get("User", data["user_id"])
    if not u:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    pl = Place(**data)
    pl.city_id = city_id
    pl.save()
    return make_response(jsonify(pl.to_dict()), 201)


@app_views.route("/places/<place_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """
    Updates a Place object, with all key-value pairs
    of the dictionary.
    If the place_id is not linked to any Place object,
        raise a 404 error.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    Returns the Place object with the status code 200.
    """
    pl = storage.get("Place", place_id)
    if not pl:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for k, v in data.items():
        if k not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(pl, k, v)
    pl.save()
    return make_response(jsonify(pl.to_dict()), 200)


@app_views.route("/places_search",
                 methods=["POST"],
                 strict_slashes=False)
def places_search():
    """
    retrieves all Place objects depending
    of the JSON in the body of the request.
    """
    data = request.get_json()
    l_pl = []
    if not data:
        abort(400, description="Not a JSON")
    if data and len(data):
        am = data.get("amenities", None)
        ct = data.get("cities", None)
        st = data.get("states", None)
    if not data or not len(data) or (
            not am and not ct and not st):
        pl = storage.all(Place).values()
        for p in pl:
            l_pl.append(p.to_dict())
        return jsonify(l_pl)
