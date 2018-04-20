"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed
        """

        return "<User user_id={} email={}>".format(self.user_id, self.email)


# Put your Movie and Rating model classes here.

class Movie(db.Model):
    """A movie; stored in a database."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    released_at = db.Column(db.DateTime, nullable=False)
    imdb_url = db.Column(db.String(500), nullable=True)

    @classmethod
    def get_by_movie_id(cls, movie_id):
        """Get a movie from database by ID and return instance."""

        QUERY = """SELECT movie_id, title, released_at, imdb_url
                   FROM movie WHERE movie_id = :movie_id"""
        cursor = db.session.execute(QUERY, {'movie_id': movie_id})
        movie_id, title, released_at, imdb_url = cursor.fetchone()
        return cls(movie_id, title, released_at, imdb_url)

    def __repr__(self):
        """Provide helpful representation when printed
        """

        return "<User movie_id={} title={} released_at={} imdb_url={}>".format(self.movie_id, self.title, self.released_at, self.imdb_url)


class Rating(db.Model):
    """A rating of a movie; stored in a database."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    @classmethod
    def get_by_rating_id(cls, rating_id):
        """Get a rating from database by ID and return instance."""

        QUERY = """SELECT rating_id, movie_id, user_id, score
                   FROM rating WHERE rating_id = :rating_id"""
        cursor = db.session.execute(QUERY, {'rating_id': rating_id})
        rating_id, movie_id, user_id, score = cursor.fetchone()
        return cls(rating_id, movie_id, user_id, score)

    def __repr__(self):
        """Provide helpful representation when printed
        """

        return "<rating_id={} movie_id={} user_id={} score={}>".format(self.rating_id, self.movie_id, self.user_id, self.score)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
