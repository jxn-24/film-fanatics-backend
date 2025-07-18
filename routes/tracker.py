from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.tracker import Tracker

tracker_bp = Blueprint('tracker', __name__, url_prefix='/api/tracker')

@tracker_bp.route('/', methods=['POST'])
@jwt_required()
def add_tracker():
    data = request.get_json()
    movie_title = data.get('movie_title')
    status = data.get('status')
    user_id = get_jwt_identity()

    tracker = Tracker(movie_title=movie_title, status=status, user_id=user_id)
    db.session.add(tracker)
    db.session.commit()

    return jsonify(tracker.to_dict()), 201

@tracker_bp.route('/', methods=['GET'])
@jwt_required()
def get_tracker():
    user_id = get_jwt_identity()
    records = Tracker.query.filter_by(user_id=user_id).all()
    return jsonify([t.to_dict() for t in records])
