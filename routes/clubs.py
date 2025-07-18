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
    name, genre = data.get('name'), data.get('genre')
    user_id = get_jwt_identity()

    club = Club(name=name, genre=genre)
    club.members.append(User.query.get(user_id))
    db.session.add(club)
    db.session.commit()

    return jsonify(club.to_dict()), 201

@clubs_bp.route('/', methods=['GET'])
def list_clubs():
    return jsonify([c.to_dict() for c in Club.query.all()])
