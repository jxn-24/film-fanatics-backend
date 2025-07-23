from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.post import Post

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')

@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()

    new_post = Post(
        title=data['title'],
        content=data['content'],
        movie_id=data.get('movie_id'),
        movie_title=data.get('movie_title'),
        movie_poster_url=data.get('movie_poster_url'),
        club_id=data.get('club_id'),
        user_id=user_id
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201

@posts_bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts]), 200

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict()), 200

@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    if post.user_id != get_jwt_identity():
        return jsonify({'msg': 'Unauthorized'}), 403
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()
    return jsonify(post.to_dict()), 200

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != get_jwt_identity():
        return jsonify({'msg': 'Unauthorized'}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({'msg': 'Deleted'}), 200  # Changed from 204 to 200
