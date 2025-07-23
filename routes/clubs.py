from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.club import Club
from models.user import User

clubs_bp = Blueprint('clubs', __name__, url_prefix='/api/clubs')

@clubs_bp.route('/', methods=['POST'])
@jwt_required()
def create_club():
    data = request.get_json()
    user_id = get_jwt_identity()

  
    if not all(key in data for key in ['name', 'genre', 'description']):
        return jsonify({'error': 'Missing required club fields'}), 400

    try:
        club = Club(
            name=data['name'],
            genre=data['genre'],
            description=data['description'],
            owner_id=user_id  
        )
        db.session.add(club)
        db.session.commit()
        return jsonify({'message': 'Club created successfully', 'club_id': club.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
