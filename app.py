# app.py
from flask import Flask, jsonify
from config import config
from extensions import db, bcrypt, jwt, migrate

# Import all blueprints
from routes.auth import auth_bp
from routes.users import users_bp
from routes.clubs import clubs_bp
from routes.posts import posts_bp
from routes.comments import comments_bp
from routes.tracker import tracker_bp
# from routes.ratings import ratings_bp  # Optional if ratings.py exists

# Import models for migrations
from models.user import User
from models.rating import Rating
from models.club import Club
from models.comment import Comment
from models.post import Post
from models.tracker import Tracker
# from models.movie import Movie  # Uncomment if you have this model

# Initialize app
app = Flask(__name__)
env = config['development']
app.config.from_object(env)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(clubs_bp, url_prefix='/api/clubs')
app.register_blueprint(posts_bp, url_prefix='/api/posts')
app.register_blueprint(comments_bp, url_prefix='/api/comments')
app.register_blueprint(tracker_bp, url_prefix='/api/tracker')
app.register_blueprint(ratings_bp, url_prefix='/api/ratings')  # Optional

# Default route
@app.route('/')
def index():
    return {"message": "🎬 Film Fanatics API is running!"}

# ✅ TEMP route to test JWT token generation
@app.route('/test-token')
def test_token():
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=1)
    return jsonify({"token": token})


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
