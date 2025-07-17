from flask import Flask
from config import config
from extensions import db, bcrypt, jwt

from routes.auth import auth_bp
from routes.users import users_bp
from routes.clubs import clubs_bp
from routes.posts import posts_bp
from routes.comments import comments_bp
from routes.tracker import tracker_bp

app = Flask(__name__)
env = config['development']
app.config.from_object(env)

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)


app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(clubs_bp, url_prefix='/api/clubs')
app.register_blueprint(posts_bp, url_prefix='/api/posts')
app.register_blueprint(comments_bp, url_prefix='/api/comments')
app.register_blueprint(tracker_bp, url_prefix='/api/tracker')


app.register_blueprint(auth_bp, url_prefix="/api/auth")


@app.route('/')
def index():
    return {"message": "Film Fanatics API is live 🎬"}

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
