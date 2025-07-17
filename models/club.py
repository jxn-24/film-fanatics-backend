from extensions import db
from datetime import datetime
from models.user import club_members

class Club(db.Model):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', backref=db.backref('owned_clubs', lazy=True))
    posts = db.relationship('Post', backref='club', lazy=True, cascade="all, delete-orphan")

    members = db.relationship('User', secondary=club_members, back_populates='clubs')

    def __repr__(self):
        return f'<Club {self.name}>'