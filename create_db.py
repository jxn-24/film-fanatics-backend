from app import app
from extensions import db
import models

with app.app_context():
    db.create_all()
    print("✅ app.db created successfully!")
