from werkzeug.security import check_password_hash, generate_password_hash

import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_movies(user_id):
    sql = """SELECT movies.id, movies.title, movies.year,
                    AVG(reviews.rating) avg_rating,
                    COUNT(reviews.id) review_count
             FROM movies
             LEFT JOIN reviews ON movies.id = reviews.movie_id
             WHERE movies.user_id = ?
             GROUP BY movies.id
             ORDER BY movies.id DESC"""
    return db.query(sql, [user_id])

def get_movie_count(user_id):
    sql = "SELECT COUNT(*) FROM movies WHERE user_id = ?"
    return db.query(sql, [user_id])[0][0]

def get_review_count(user_id):
    sql = "SELECT COUNT(*) FROM reviews WHERE user_id = ?"
    return db.query(sql, [user_id])[0][0]

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    return None
