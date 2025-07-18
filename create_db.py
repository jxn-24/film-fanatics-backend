from app import app
from extensions import db
import models  # Make sure all models are imported in this module

with app.app_context():
    db.create_all()
    print("✅ app.db created successfully!")
