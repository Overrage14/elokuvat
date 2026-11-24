"""Database operations for movies and their classifications."""

import re

from flask import abort

import db

def get_all_genres():
    """Return all genres ordered by ID."""
    sql = "SELECT id, name FROM genres ORDER BY id"
    return db.query(sql)

def get_all_age_ratings():
    """Return all age ratings ordered by ID."""
    sql = "SELECT id, name FROM age_ratings ORDER BY id"
    return db.query(sql)

def validate_movie_data(form):
    """Validate movie form data and return values and errors."""
    title = form.get("title", "").strip()
    year = form.get("year", "").strip()
    description = form.get("description", "").strip()
    errors = []

    if not title:
        errors.append("VIRHE: lisää elokuvan nimi")
    elif len(title) > 50:
        errors.append("VIRHE: elokuvan nimi voi olla enintään 50 merkkiä")

    if not re.search("^[0-9]{4}$", year):
        errors.append("VIRHE: lisää kelvollinen valmistumisvuosi (1888-2100)")
    elif not 1888 <= int(year) <= 2100:
        errors.append("VIRHE: valmistumisvuoden tulee olla välillä 1888-2100")

    if not description:
        errors.append("VIRHE: lisää kuvaus")
    elif len(description) > 1000:
        errors.append("VIRHE: kuvaus voi olla enintään 1000 merkkiä")

    return title, year, description, errors

def get_selected_genres(form):
    """Return the validated genre IDs selected in the form."""
    valid_ids = {genre["id"] for genre in get_all_genres()}
    genre_ids = []
    for entry in form.getlist("genres"):
        entry = entry.strip()
        if entry:
            if not entry.isdigit() or int(entry) not in valid_ids:
                abort(403)
            genre_ids.append(int(entry))
    return genre_ids

def get_selected_age_rating(form):
    """Return the validated age rating selected in the form."""
    valid_ids = {age_rating["id"] for age_rating in get_all_age_ratings()}
    entry = form.get("age_rating", "").strip()
    if not entry:
        return None
    if not entry.isdigit() or int(entry) not in valid_ids:
        abort(403)
    return int(entry)

def get_movie(movie_id):
    """Return a movie with its owner, or None if not found."""
    sql = """SELECT movies.id, movies.title, movies.year, movies.description,
                    users.id user_id, users.username
             FROM movies, users
             WHERE movies.user_id = users.id AND movies.id = ?"""
    result = db.query(sql, [movie_id])
    return result[0] if result else None

def get_genres(movie_id):
    """Return the genres of a movie."""
    sql = """SELECT genres.id, genres.name
             FROM genres, movie_genres
             WHERE genres.id = movie_genres.genre_id AND
                   movie_genres.movie_id = ?
             ORDER BY genres.id"""
    return db.query(sql, [movie_id])

def get_age_ratings(movie_id):
    """Return the age ratings of a movie."""
    sql = """SELECT age_ratings.id, age_ratings.name
             FROM age_ratings, movie_age_ratings
             WHERE age_ratings.id = movie_age_ratings.age_rating_id AND
                   movie_age_ratings.movie_id = ?
             ORDER BY age_ratings.id"""
    return db.query(sql, [movie_id])

def add_movie(title, year, description, user_id, genre_ids, age_rating_id):
    """Add a movie and its classifications, and return its ID."""
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
    """Update a movie and replace its classifications."""
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
    """Remove a movie and all data that references it."""
    sql = "DELETE FROM reviews WHERE movie_id = ?"
    db.execute(sql, [movie_id])
    sql = "DELETE FROM movie_genres WHERE movie_id = ?"
    db.execute(sql, [movie_id])
    sql = "DELETE FROM movie_age_ratings WHERE movie_id = ?"
    db.execute(sql, [movie_id])
    sql = "DELETE FROM movies WHERE id = ?"
    db.execute(sql, [movie_id])

def find_conditions(query, genre_id):
    """Build WHERE conditions and parameters for movie search."""
    # Builds the WHERE conditions for keyword and genre search. The
    # conditions are fixed strings and all values are given as
    # parameters, so the dynamic construction is safe.
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
    return conditions, params

def find_movies_count(query, genre_id):
    """Return the number of movies matching the search."""
    conditions, params = find_conditions(query, genre_id)
    sql = "SELECT COUNT(*) FROM movies"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    return db.query(sql, params)[0][0]

def find_movies(query, genre_id, page, page_size):
    """Return one page of movies matching the search."""
    conditions, params = find_conditions(query, genre_id)
    sql = """SELECT movies.id, movies.title, movies.year,
                    users.id user_id, users.username
             FROM movies
             JOIN users ON movies.user_id = users.id"""
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY movies.id DESC LIMIT ? OFFSET ?"
    params.append(page_size)
    params.append((page - 1) * page_size)
    return db.query(sql, params)

def get_movies_count():
    """Return the total number of movies."""
    sql = "SELECT COUNT(*) FROM movies"
    return db.query(sql)[0][0]

def get_movies(page, page_size):
    """Return one page of movies with review statistics."""
    offset = (page - 1) * page_size
    sql = """SELECT movies.id, movies.title, movies.year,
                    users.id user_id, users.username,
                    AVG(reviews.rating) avg_rating,
                    COUNT(reviews.id) review_count
             FROM movies
             JOIN users ON movies.user_id = users.id
             LEFT JOIN reviews ON movies.id = reviews.movie_id
             GROUP BY movies.id
             ORDER BY movies.id DESC
             LIMIT ? OFFSET ?"""
    return db.query(sql, [page_size, offset])
