from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.post import Post
from models.user import User

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')

@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    user_id = get_jwt_identity()
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict()), 201

@posts_bp.route('/', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])
