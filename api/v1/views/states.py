#!/usr/bin/python3
"""
Create new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort
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
