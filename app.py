from flask import Flask
from config import config
from extensions import db, bcrypt, jwt

from routes.auth import auth_bp  # ✅ import your test route

app = Flask(__name__)
env = config['development']
app.config.from_object(env)

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# Register blueprint
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
