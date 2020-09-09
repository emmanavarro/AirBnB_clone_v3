#!/usr/bin/python3
"""
Create new view for City objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User


@app_views.route('/users',
                 strict_slashes=False, methods=['GET'])
def users():
    """
    Retrieve all users
    """
    users_obj = storage.all("User")
    all_users = [user.to_dict() for user in users_obj.values()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def get_users(user_id):
    """
    Retrieve users by Id
    """
    users_id = storage.get("User", user_id)
    if users_id:
        return jsonify(users_id.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_users(user_id):
    """
    Deletes an user object by its Id
    """
    users_id = storage.get("User", user_id)
    if users_id:
        storage.delete(users_id)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False,
                 methods=['POST'])
def post_users():
    """
    Creates an User object
    """
    json_request = request.get_json()
    if not json_request:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'email' not in json_request:
        return jsonify({'email': 'Missing email'}), 400
    elif 'password' not in json_request:
        return jsonify({'password': 'Missing password'}), 400
    else:
        new_user = User(**json_request)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def put_users(user_id):
    """
    Updates a User object by its Id
    """
    json_request = request.get_json()
    if not json_request:
        return jsonify({'error': 'Not a JSON'}), 400
    user_id = storage.get("User", user_id)
    if user_id:
        for key, value in json_request.items():
            setattr(user_id, key, value)
        storage.save()
        return jsonify(user_id.to_dict()), 200
    else:
        abort(404)
