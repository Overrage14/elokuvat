import db

def get_all_genres():
    sql = "SELECT id, name FROM genres ORDER BY id"
    return db.query(sql)

def get_all_age_ratings():
    sql = "SELECT id, name FROM age_ratings ORDER BY id"
    return db.query(sql)

def add_movie(title, year, description, user_id, genre_ids, age_rating_id):
    sql = """INSERT INTO movies (title, year, description, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, year, description, user_id])

    movie_id = db.last_insert_id()

    sql = "INSERT INTO movie_genres (movie_id, genre_id) VALUES (?, ?)"
    for genre_id in genre_ids:
        db.execute(sql, [movie_id, genre_id])

    if age_rating_id:
        sql = """INSERT INTO movie_age_ratings (movie_id, age_rating_id)
                 VALUES (?, ?)"""
        db.execute(sql, [movie_id, age_rating_id])

    return movie_id

def get_movies():
    sql = """SELECT movies.id, movies.title, movies.year,
                    users.id user_id, users.username
             FROM movies
             JOIN users ON movies.user_id = users.id
             ORDER BY movies.id DESC"""
    return db.query(sql)
