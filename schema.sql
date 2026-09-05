CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    year INTEGER,
    description TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER REFERENCES movies,
    user_id INTEGER REFERENCES users,
    rating INTEGER,
    comment TEXT
);

CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE age_ratings (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE movie_genres (
    movie_id INTEGER REFERENCES movies,
    genre_id INTEGER REFERENCES genres,
    UNIQUE (movie_id, genre_id)
);

CREATE TABLE movie_age_ratings (
    movie_id INTEGER REFERENCES movies,
    age_rating_id INTEGER REFERENCES age_ratings,
    UNIQUE (movie_id, age_rating_id)
);

CREATE INDEX idx_movies_title ON movies (title);
CREATE INDEX idx_movies_user_id ON movies (user_id);
CREATE INDEX idx_reviews_movie_id ON reviews (movie_id);
CREATE INDEX idx_movie_genres_movie_id ON movie_genres (movie_id);
