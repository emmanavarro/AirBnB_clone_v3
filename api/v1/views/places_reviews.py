#!/usr/bin/python3
"""
Create new view for Reviews objects that handles all default
RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def reviews(place_id):
    """
    Retrieve all reviews
    """
    places_obj = storage.get("Place", place_id)
    if places_obj:
        all_reviews = [review.to_dict() for review in places_obj.reviews]
        return jsonify(all_reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_reviews(review_id):
    """
    Retrieve review by Id
    """
    reviews_id = storage.get("Review", review_id)
    if reviews_id:
        return jsonify(reviews_id.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_reviews(review_id):
    """
    Deletes a review object by its Id
    """
    reviews_id = storage.get("Review", review_id)
    if reviews_id:
        storage.delete(reviews_id)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def post_reviews(place_id):
    """
    Creates a Review object
    """
    places_id = storage.get("Place", place_id)
    if places_id is None:
        abort(404)
    json_request = request.get_json()
    if not json_request:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'user_id' not in json_request:
        return jsonify({'error': 'Missing user_id'}), 400
    user_id = request.get_json()['user_id']
    users_id = storage.get("User", user_id)
    if users_id is None:
        abort(404)
    if 'text' not in json_request:
        return jsonify({'error': 'Missing text'}), 400
    else:
        new_review = Review(**json_request)
        new_review.place_id = place_id
        new_review.user_id = user_id
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def put_reviews(review_id):
    """
    Updates a Review object by its Id
    """
    json_request = request.get_json()
    if not json_request:
        return jsonify({'error': 'Not a JSON'}), 400
    reviews_id = storage.get("Review", review_id)
    if reviews_id:
        for key, value in json_request.items():
            setattr(reviews_id, key, value)
        storage.save()
        return jsonify(reviews_id.to_dict()), 200
    else:
        abort(404)
