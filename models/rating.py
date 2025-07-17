from extensions import db
from datetime import datetime

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.String(50), nullable=False)
    movie_title = db.Column(db.String(200))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='_user_movie_uc'),)

    def __repr__(self):
        return f'<Rating {self.score} for movie {self.movie_id} by user {self.user_id}>'