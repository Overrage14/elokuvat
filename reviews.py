import db

def get_reviews(movie_id):
    sql = """SELECT reviews.id, reviews.rating, reviews.comment,
                    users.id user_id, users.username
             FROM reviews, users
             WHERE reviews.movie_id = ? AND reviews.user_id = users.id
             ORDER BY reviews.id DESC"""
    return db.query(sql, [movie_id])

def get_average_rating(movie_id):
    sql = "SELECT AVG(rating) FROM reviews WHERE movie_id = ?"
    result = db.query(sql, [movie_id])
    return result[0][0]

def add_review(movie_id, user_id, rating, comment):
    sql = """INSERT INTO reviews (movie_id, user_id, rating, comment)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [movie_id, user_id, rating, comment])
