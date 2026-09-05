import db

def get_all_genres():
    sql = "SELECT id, name FROM genres ORDER BY id"
    return db.query(sql)

def get_all_age_ratings():
    sql = "SELECT id, name FROM age_ratings ORDER BY id"
    return db.query(sql)

def get_movies():
    sql = """SELECT movies.id, movies.title, movies.year,
                    users.id user_id, users.username
             FROM movies
             JOIN users ON movies.user_id = users.id
             ORDER BY movies.id DESC"""
    return db.query(sql)
