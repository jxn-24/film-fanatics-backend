from flask import Blueprint, request, jsonify
from models.tracker import Tracker
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

tracker_bp = Blueprint('tracker', __name__, url_prefix='/api/tracker')

@tracker_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_watchlist():
    user_id = get_jwt_identity()
    items = Tracker.query.filter_by(user_id=user_id).all()
    return jsonify([item.to_dict() for item in items]), 200

@tracker_bp.route('/', methods=['POST'])
@jwt_required()
def add_to_watchlist():
    data = request.json
    user_id = get_jwt_identity()
    item = Tracker(user_id=user_id, movie_title=data['movie_title'], status=data['status'])
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201
