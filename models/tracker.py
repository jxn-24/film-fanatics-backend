from extensions import db
from datetime import datetime

class Tracker(db.Model):
    __tablename__ = 'trackers'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    watched_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.String(50), nullable=False)
    movie_title = db.Column(db.String(200), nullable=False)
    movie_poster_url = db.Column(db.String(255))

    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='_user_movie_tracker_uc'),)

    def __repr__(self):
        return f'<Tracker User:{self.user_id} Movie:{self.movie_title} Status:{self.status}>'