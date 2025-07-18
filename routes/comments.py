from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.comment import Comment

comments_bp = Blueprint('comments', __name__, url_prefix='/api/comments')

@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    post_id = data.get('post_id')
    content = data.get('content')
    user_id = get_jwt_identity()

    comment = Comment(post_id=post_id, content=content, user_id=user_id)
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201

@comments_bp.route('/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return jsonify([c.to_dict() for c in comments])
