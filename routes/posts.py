from flask import Blueprint, request, jsonify
from models.post import Post
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')

@posts_bp.route('/', methods=['GET'])
def list_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts]), 200

@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.json
    user_id = get_jwt_identity()
    post = Post(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201
