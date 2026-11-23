"""Database operations for user accounts."""

from werkzeug.security import check_password_hash, generate_password_hash

import db

def get_user(user_id):
    """Return a user by ID, or None if not found."""
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_movies(user_id, page, page_size):
    """Return one page of a user's movies with review statistics."""
    offset = (page - 1) * page_size
    sql = """SELECT movies.id, movies.title, movies.year,
                    AVG(reviews.rating) avg_rating,
                    COUNT(reviews.id) review_count
             FROM movies
             LEFT JOIN reviews ON movies.id = reviews.movie_id
             WHERE movies.user_id = ?
             GROUP BY movies.id
             ORDER BY movies.id DESC
             LIMIT ? OFFSET ?"""
    return db.query(sql, [user_id, page_size, offset])

def get_movie_count(user_id):
    """Return the number of movies added by a user."""
    sql = "SELECT COUNT(*) FROM movies WHERE user_id = ?"
    return db.query(sql, [user_id])[0][0]

def get_review_count(user_id):
    """Return the number of reviews written by a user."""
    sql = "SELECT COUNT(*) FROM reviews WHERE user_id = ?"
    return db.query(sql, [user_id])[0][0]

def create_user(username, password):
    """Create a new user with a hashed password and return the user ID."""
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])
    return db.last_insert_id()

def check_login(username, password):
    """Return the user ID if the credentials are valid."""
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    return None
