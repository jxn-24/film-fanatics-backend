from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.rating import Rating

ratings_bp = Blueprint('ratings', __name__, url_prefix='/api/ratings')


@ratings_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_ratings():
    user_id = get_jwt_identity()
    ratings = Rating.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': r.id,
        'score': r.score,
        'movie_id': r.movie_id,
        'movie_title': r.movie_title,
        'post_id': r.post_id,
        'created_at': r.created_at,
        'updated_at': r.updated_at
    } for r in ratings]), 200


@ratings_bp.route('/', methods=['POST'])
@jwt_required()
def create_rating():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Require all essential fields
    required_fields = ['score', 'movie_id', 'movie_title', 'post_id']
    if not all(field in data and data[field] is not None for field in required_fields):
        return jsonify({"error": "score, movie_id, movie_title, and post_id are required"}), 400

    # Prevent duplicate rating
    existing_rating = Rating.query.filter_by(user_id=user_id, movie_id=data['movie_id']).first()
    if existing_rating:
        return jsonify({"error": "You have already rated this movie"}), 409

    # Create and save the rating
    rating = Rating(
        score=data['score'],
        user_id=user_id,
        movie_id=data['movie_id'],
        movie_title=data['movie_title'],
        post_id=data['post_id']
    )
    db.session.add(rating)
    db.session.commit()

    return jsonify({
        'id': rating.id,
        'score': rating.score,
        'movie_id': rating.movie_id,
        'movie_title': rating.movie_title,
        'post_id': rating.post_id,
        'created_at': rating.created_at,
        'updated_at': rating.updated_at
    }), 201


@ratings_bp.route('/<int:rating_id>', methods=['PUT'])
@jwt_required()
def update_rating(rating_id):
    rating = Rating.query.get_or_404(rating_id)
    user_id = get_jwt_identity()

    if rating.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if 'score' in data:
        rating.score = data['score']
    if 'movie_title' in data:
        rating.movie_title = data['movie_title']
    if 'post_id' in data:
        rating.post_id = data['post_id']

    db.session.commit()
    return jsonify({
        'id': rating.id,
        'score': rating.score,
        'movie_id': rating.movie_id,
        'movie_title': rating.movie_title,
        'post_id': rating.post_id,
        'created_at': rating.created_at,
        'updated_at': rating.updated_at
    }), 200


@ratings_bp.route('/<int:rating_id>', methods=['DELETE'])
@jwt_required()
def delete_rating(rating_id):
    rating = Rating.query.get_or_404(rating_id)
    user_id = get_jwt_identity()

    if rating.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(rating)
    db.session.commit()
    return jsonify({"message": "Rating deleted"}), 204
