from flask import Flask
from config import config
from extensions import db, bcrypt, jwt

app = Flask(__name__)
env = config['development']  # Default to development for now
app.config.from_object(env)

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])