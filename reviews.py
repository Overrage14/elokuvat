"""Database operations for movie reviews."""

import db

def get_reviews(movie_id):
    """Return the reviews of a movie with reviewer names."""
    sql = """SELECT reviews.id, reviews.rating, reviews.comment,
                    users.id user_id, users.username
             FROM reviews, users
             WHERE reviews.movie_id = ? AND reviews.user_id = users.id
             ORDER BY reviews.id DESC"""
    return db.query(sql, [movie_id])

def get_average_rating(movie_id):
    """Return the average rating of a movie."""
    sql = "SELECT AVG(rating) FROM reviews WHERE movie_id = ?"
    result = db.query(sql, [movie_id])
    return result[0][0]

def get_review_count(movie_id):
    """Return the number of reviews for a movie."""
    sql = "SELECT COUNT(*) FROM reviews WHERE movie_id = ?"
    return db.query(sql, [movie_id])[0][0]

def get_review(review_id):
    """Return a review with the movie title, or None if not found."""
    sql = """SELECT reviews.id, reviews.movie_id, reviews.user_id,
                    reviews.rating, reviews.comment, movies.title movie_title
             FROM reviews, movies
             WHERE reviews.movie_id = movies.id AND reviews.id = ?"""
    result = db.query(sql, [review_id])
    return result[0] if result else None

def add_review(movie_id, user_id, rating, comment):
    """Add a review to a movie."""
    sql = """INSERT INTO reviews (movie_id, user_id, rating, comment)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [movie_id, user_id, rating, comment])

def update_review(review_id, rating, comment):
    """Update the rating and comment of a review."""
    sql = "UPDATE reviews SET rating = ?, comment = ? WHERE id = ?"
    db.execute(sql, [rating, comment, review_id])

def remove_review(review_id):
    """Remove a review."""
    sql = "DELETE FROM reviews WHERE id = ?"
    db.execute(sql, [review_id])
