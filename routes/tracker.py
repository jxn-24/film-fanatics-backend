from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.tracked_movie import TrackedMovie  

tracker_bp = Blueprint('tracker', __name__, url_prefix='/api/tracker')


@tracker_bp.route('/', methods=['GET'])
@jwt_required()
def get_tracked():
    user_id = get_jwt_identity()
    tracked = TrackedMovie.query.filter_by(user_id=user_id).all()
    return jsonify([t.to_dict() for t in tracked]), 200


@tracker_bp.route('/', methods=['POST'])
@jwt_required()
def add_tracked():
    data = request.get_json()
    user_id = get_jwt_identity()

    required_fields = ['movie_id', 'movie_title', 'poster_url', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    tracked = TrackedMovie(
        user_id=user_id,
        movie_id=data['movie_id'],
        movie_title=data['movie_title'],
        poster_url=data['poster_url'],
        status=data['status']
    )

    db.session.add(tracked)
    db.session.commit()
    return jsonify(tracked.to_dict()), 201


@tracker_bp.route('/<int:track_id>', methods=['PUT'])
@jwt_required()
def update_tracked(track_id):
    tracked = TrackedMovie.query.get_or_404(track_id)
    user_id = get_jwt_identity()

    if tracked.user_id != user_id:
        return jsonify({'msg': 'Unauthorized'}), 403

    data = request.get_json()
    if 'status' in data:
        tracked.status = data['status']
    db.session.commit()
    return jsonify(tracked.to_dict()), 200


@tracker_bp.route('/<int:track_id>', methods=['DELETE'])
@jwt_required()
def delete_tracked(track_id):
    tracked = TrackedMovie.query.get_or_404(track_id)
    user_id = get_jwt_identity()

    if tracked.user_id != user_id:
        return jsonify({'msg': 'Unauthorized'}), 403

    db.session.delete(tracked)
    db.session.commit()
    return jsonify({'msg': 'Deleted'}), 204
