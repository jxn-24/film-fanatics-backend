from flask import Blueprint, request, jsonify
from models.club import Club
from extensions import db
from flask_jwt_extended import jwt_required

clubs_bp = Blueprint('clubs', __name__, url_prefix='/api/clubs')

@clubs_bp.route('/', methods=['GET'])
def list_clubs():
    clubs = Club.query.all()
    return jsonify([club.to_dict() for club in clubs]), 200

@clubs_bp.route('/', methods=['POST'])
@jwt_required()
def create_club():
    data = request.json
    club = Club(name=data['name'], genre=data['genre'])
    db.session.add(club)
    db.session.commit()
    return jsonify(club.to_dict()), 201
