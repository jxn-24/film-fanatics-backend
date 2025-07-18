# extensions.py
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_bcrypt import Bcrypt # type: ignore
from flask_jwt_extended import JWTManager # type: ignore
from flask_migrate import Migrate  # type: ignore # ✅ MUST be imported

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()  # ✅ MUST be created
