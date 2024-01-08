#!/usr/bin/python3
<<<<<<< HEAD
"""A script that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
=======
"""
flask RESTful API
    GET /api/v1/states
    GET /api/v1/states/<state_id>
    DELETE /api/v1/states/<state_id>
    POST /api/v1/states
    PUT /api/v1/states/<state_id>
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
>>>>>>> 4b1746cd0e8b61be00cbf36bea1f619dc10b66d5
from models import storage
from models.state import State


<<<<<<< HEAD
@app_views.route("/states")
def states():
    """Retrieve the list of all `State` objects"""
    result = []
    for value in storage.all(State).values():
        result.append(value.to_dict())
    return jsonify(result)


@app_views.route("/states/<state_id>")
def state(state_id: str):
    """Retrive one state object

    Args:
        state_id (string): state identifier

    Returns:
        Response: `State` object in json
    """
    result = storage.get(State, state_id)
    if result is None:
        abort(404)
    return jsonify(result.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Delete a state object

    Args:
        state_id (str): state identifier

    Returns:
        Response: Empty dictionary - `{}`
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states", methods=["POST"])
def create_state():
    """Create a `State` object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Update `State` object

    Args:
        state_id (str): state identifier

    Returns:
        Response: `State` object with status code 200
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    key = "name"
    setattr(state, key, request.get_json().get(key))
    state.save()
    return jsonify(state.to_dict())
=======
@app_views.route("/states",
                 methods=["GET"],
                 strict_slashes=False)
def get_all_states():
    """
    Retrieves the list of all State objects.
    """
    for st in storage.all(State).values():
        l_states = [st.to_dict()]
    return jsonify(l_states)


@app_views.route("/states/<state_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by id. If the state_id is not
    linked to any State object, raise a 404 error.
    """
    st = storage.get("State", state_id)
    if st is None:
        abort(404)
    return jsonify(st.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object. If the state_id is not
    linked to any State object, raise a 404 error.
    Returns an empty dictionary with the status code 200.
    """
    st = storage.get("State", state_id)
    if st is None:
        abort(404)
    st.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states",
                 methods=["POST"],
                 strict_slashes=False)
def post_state():
    """
    Creates a State.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    If the dictionary doesn’t contain the key name,
        raise a 400 error with the message Missing name
    Returns the new State with the status code 201.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    elif "name" not in request.get_json():
        abort(400, description="Missing name")
    else:
        data = request.get_json()
        st = State(**data)
        st.save()
        return make_response(jsonify(st.to_dict()), 201)


@app_views.route("/states/<states_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def put_state(states_id):
    """
    Updates a State object, with all key-value pairs
    of the dictionary.
    If the state_id is not linked to any State object,
        raise a 404 error.
    If the HTTP body request is not valid JSON,
        raise a 400 error with the message Not a JSON.
    Returns the State object with the status code 200.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    st = storage.get("State", states_id)
    if st is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(st, k, v)
    st.save()
    return make_response(jsonify(st.to_dict()), 200)
>>>>>>> 4b1746cd0e8b61be00cbf36bea1f619dc10b66d5
