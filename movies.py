import db

def get_all_genres():
    sql = "SELECT id, name FROM genres ORDER BY id"
    return db.query(sql)

def get_all_age_ratings():
    sql = "SELECT id, name FROM age_ratings ORDER BY id"
    return db.query(sql)

def get_movie(movie_id):
    sql = """SELECT movies.id, movies.title, movies.year, movies.description,
                    users.id user_id, users.username
             FROM movies, users
             WHERE movies.user_id = users.id AND movies.id = ?"""
    result = db.query(sql, [movie_id])
    return result[0] if result else None

def get_genres(movie_id):
    sql = """SELECT genres.id, genres.name
             FROM genres, movie_genres
             WHERE genres.id = movie_genres.genre_id AND
                   movie_genres.movie_id = ?
             ORDER BY genres.id"""
    return db.query(sql, [movie_id])

def get_age_ratings(movie_id):
    sql = """SELECT age_ratings.id, age_ratings.name
             FROM age_ratings, movie_age_ratings
             WHERE age_ratings.id = movie_age_ratings.age_rating_id AND
                   movie_age_ratings.movie_id = ?
             ORDER BY age_ratings.id"""
    return db.query(sql, [movie_id])

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

def update_movie(movie_id, title, year, description, genre_ids, age_rating_id):
    sql = """UPDATE movies SET title = ?,
                              year = ?,
                              description = ?
                          WHERE id = ?"""
    db.execute(sql, [title, year, description, movie_id])

    sql = "DELETE FROM movie_genres WHERE movie_id = ?"
    db.execute(sql, [movie_id])
    sql = "INSERT INTO movie_genres (movie_id, genre_id) VALUES (?, ?)"
    for genre_id in genre_ids:
        db.execute(sql, [movie_id, genre_id])

    sql = "DELETE FROM movie_age_ratings WHERE movie_id = ?"
    db.execute(sql, [movie_id])
    if age_rating_id:
        sql = """INSERT INTO movie_age_ratings (movie_id, age_rating_id)
                 VALUES (?, ?)"""
        db.execute(sql, [movie_id, age_rating_id])

def remove_movie(movie_id):
    sql = "DELETE FROM reviews WHERE movie_id = ?"
    db.execute(sql, [movie_id])
    sql = "DELETE FROM movie_genres WHERE movie_id = ?"
    db.execute(sql, [movie_id])
    sql = "DELETE FROM movie_age_ratings WHERE movie_id = ?"
    db.execute(sql, [movie_id])
    sql = "DELETE FROM movies WHERE id = ?"
    db.execute(sql, [movie_id])

def find_movies(query, genre_id):
    sql = """SELECT movies.id, movies.title, movies.year,
                    users.id user_id, users.username
             FROM movies
             JOIN users ON movies.user_id = users.id"""
    conditions = []
    params = []
    if query:
        conditions.append("(movies.title LIKE ? OR movies.description LIKE ?)")
        like = "%" + query + "%"
        params.append(like)
        params.append(like)
    if genre_id:
        conditions.append("""movies.id IN (SELECT movie_id FROM movie_genres
                                           WHERE genre_id = ?)""")
        params.append(genre_id)
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY movies.id DESC"
    return db.query(sql, params)

def get_movies():
    sql = """SELECT movies.id, movies.title, movies.year,
                    users.id user_id, users.username,
                    AVG(reviews.rating) avg_rating,
                    COUNT(reviews.id) review_count
             FROM movies
             JOIN users ON movies.user_id = users.id
             LEFT JOIN reviews ON movies.id = reviews.movie_id
             GROUP BY movies.id
             ORDER BY movies.id DESC"""
    return db.query(sql)
