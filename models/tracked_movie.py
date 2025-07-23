from extensions import db

class TrackedMovie(db.Model):
    __tablename__ = 'tracked_movies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    movie_title = db.Column(db.String(255), nullable=False)
    poster_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'movie_title': self.movie_title,
            'poster_url': self.poster_url,
            'status': self.status
        }
