from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from extensions import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email
    } for user in users]), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
        "profile_picture": user.profile_picture
    })

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    current_user_id = get_jwt_identity()
    if user.id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    user.username = data.get("username", user.username)
    user.bio = data.get("bio", user.bio)
    user.profile_picture = data.get("profile_picture", user.profile_picture)

    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    current_user_id = get_jwt_identity()
    if user.id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})
