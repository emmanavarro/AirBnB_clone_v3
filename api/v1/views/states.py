#!/usr/bin/python3
"""
Create new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """
    Retrieve all states
    """
    states_obj = storage.all("State")
    all_states = [state.to_dict() for state in states_obj.values()]
    return jsonify(all_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_states(state_id):
    """
    Retrieve states by Id
    """
    states_id = storage.get("State", state_id)
    if states_id:
        return jsonify(states_id.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_states(state_id):
    """
    Deletes a state object by its Id
    """
    states_id = storage.get("State", state_id)
    if states_id:
        storage.delete(states_id)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """
    Creates a State object
    """
    json_request = request.get_json()
    if not json_request:
        return json_request({'error': 'Not a JSON'}), 400
    elif 'name' not in json_request:
        return json_request({'error': 'Missing name'}), 400
    else:
        new_state = State(**json_request)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    """
    Updates a State object by its Id
    """
    json_request = request.get_json()
    if not json_request:
        return json_request({'error': 'Not a JSON'}), 400
    states_id = storage.get("State", state_id)
    if states_id:
        for key, value in json_request.items():
            setattr(states_id, key, value)
        storage.save()
        return jsonify(states_id.to_dict()), 200
    else:
        abort(404)
