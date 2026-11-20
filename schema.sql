CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER NOT NULL CHECK (year BETWEEN 1888 AND 2100),
    description TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    movie_id INTEGER NOT NULL REFERENCES movies,
    user_id INTEGER NOT NULL REFERENCES users,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 10),
    comment TEXT NOT NULL,
    UNIQUE (movie_id, user_id)
);

CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE age_ratings (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE movie_genres (
    movie_id INTEGER NOT NULL REFERENCES movies,
    genre_id INTEGER NOT NULL REFERENCES genres,
    UNIQUE (movie_id, genre_id)
);

CREATE TABLE movie_age_ratings (
    movie_id INTEGER NOT NULL REFERENCES movies,
    age_rating_id INTEGER NOT NULL REFERENCES age_ratings,
    UNIQUE (movie_id)
);

CREATE INDEX idx_movies_title ON movies (title);
CREATE INDEX idx_movies_user_id ON movies (user_id);
CREATE INDEX idx_reviews_movie_id ON reviews (movie_id);
CREATE INDEX idx_reviews_user_id ON reviews (user_id);
CREATE INDEX idx_movie_genres_movie_id ON movie_genres (movie_id);
