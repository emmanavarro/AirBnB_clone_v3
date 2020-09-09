#!/usr/bin/python3
"""
Create new view for City objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def cities(state_id):
    """
    Retrieve all cities
    """
    states_obj = storage.get("State", state_id)
    if states_obj:
        all_cities = [city.to_dict() for city in states_obj.cities]
        return jsonify(all_cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def get_cities(city_id):
    """
    Retrieve cities by Id
    """
    cities_id = storage.get("City", city_id)
    if cities_id:
        return jsonify(cities_id.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_cities(city_id):
    """
    Deletes a city object by its Id
    """
    cities_id = storage.get("City", city_id)
    if cities_id:
        storage.delete(cities_id)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def post_cities(state_id):
    """
    Creates a City object
    """
    json_request = request.get_json()
    if not json_request:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in json_request:
        return jsonify({'error': 'Missing name'}), 400
    else:
        new_city = City(**json_request)
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def put_cities(city_id):
    """
    Updates a City object by its Id
    """
    json_request = request.get_json()
    if not json_request:
        return jsonify({'error': 'Not a JSON'}), 400
    cities_id = storage.get("City", city_id)
    if cities_id:
        for key, value in json_request.items():
            setattr(cities_id, key, value)
        storage.save()
        return jsonify(cities_id.to_dict()), 200
    else:
        abort(404)
