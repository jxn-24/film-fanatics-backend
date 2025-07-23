from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.comment import Comment
from models.post import Post
from models.user import User

comments_bp = Blueprint('comments', __name__, url_prefix='/api/comments')


@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    user_id = get_jwt_identity()

    post_id = data.get('post_id')
    content = data.get('content')

    if not post_id or not content:
        return jsonify({"error": "post_id and content are required"}), 400

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    comment = Comment(
        user_id=user_id,
        post_id=post_id,
        content=content
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        "id": comment.id,
        "content": comment.content,
        "user_id": comment.user_id,
        "post_id": comment.post_id,
        "created_at": comment.created_at
    }), 201


@comments_bp.route('/post/<int:post_id>', methods=['GET'])
def get_comments_for_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()

    return jsonify([
        {
            "id": c.id,
            "content": c.content,
            "user_id": c.user_id,
            "post_id": c.post_id,
            "created_at": c.created_at.isoformat()
        } for c in comments
    ]), 200


@comments_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_comment(id):
    user_id = get_jwt_identity()
    comment = Comment.query.get(id)

    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    if comment.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({"error": "Content is required"}), 400

    comment.content = content
    db.session.commit()

    return jsonify({"message": "Comment updated"}), 200


@comments_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    user_id = get_jwt_identity()
    comment = Comment.query.get(id)

    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    if comment.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comment deleted"}), 200
