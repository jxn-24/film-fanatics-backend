from extensions import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    movie_id = db.Column(db.String(50))
    movie_title = db.Column(db.String(200))
    movie_poster_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))

    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")
    ratings = db.relationship('Rating', backref='post', lazy=True, cascade="all, delete-orphan")
    likes_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Post {self.title}>'

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "movie_id": self.movie_id,
            "movie_title": self.movie_title,
            "movie_poster_url": self.movie_poster_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id,
            "club_id": self.club_id,
            "likes_count": self.likes_count,
        }
