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


@app_views.route('/amenities',
                 strict_slashes=False, methods=['GET'])
def amenities():
    """
    Retrieve all amenities
    """
    amenities_obj = storage.all("Amenity")
    all_amenities = [amenity.to_dict() for amenity in amenities_obj.values()]
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenities(amenity_id):
    """
    Retrieve amenities by Id
    """
    amenities_id = storage.get("Amenity", amenity_id)
    if amenities_id:
        return jsonify(amenities_id.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenities(amenity_id):
    """
    Deletes an amenity object by its Id
    """
    amenities_id = storage.get("Amenity", amenity_id)
    if amenities_id:
        storage.delete(amenities_id)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def post_amenities():
    """
    Creates an Amenity object
    """
    json_request = request.get_json()
    if not json_request:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in json_request:
        return jsonify({'error': 'Missing name'}), 400
    else:
        new_amenity = Amenity(**json_request)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def put_aminities(amenity_id):
    """
    Updates a Amenity object by its Id
    """
    json_request = request.get_json()
    if not json_request:
        return jsonify({'error': 'Not a JSON'}), 400
    amenity_id = storage.get("Amenity", amenity_id)
    if amenity_id:
        for key, value in json_request.items():
            setattr(amenity_id, key, value)
        storage.save()
        return jsonify(amenity_id.to_dict()), 200
    else:
        abort(404)
