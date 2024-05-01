#!/usr/bin/python3
""" Create the blueprint for Review objects """
from flask import Blueprint, jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User

app_views = Blueprint('reviews', __name__, url_prefix='/api/v1')


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def place_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def review(review_id):
    """ Retrieves a Review object """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def add_review(place_id):
    """ Creates a new Review """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400
    if data is None:
        return "Not a JSON", 400
    if 'user_id' not in data:
        return "Missing user_id", 400
    if 'text' not in data:
        return "Missing text", 400
    user_id = data.get('user_id')
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    new_review = Review(place_id=place_id, **data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        return "Not a JSON", 400
    if data is None:
        return "Not a JSON", 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
