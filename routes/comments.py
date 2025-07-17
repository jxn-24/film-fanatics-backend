from flask import Blueprint, request, jsonify
from models.comment import Comment
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

comments_bp = Blueprint('comments', __name__, url_prefix='/api/comments')

@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.json
    user_id = get_jwt_identity()
    comment = Comment(content=data['content'], post_id=data['post_id'], user_id=user_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201
