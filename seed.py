import random
import sqlite3

from werkzeug.security import generate_password_hash

user_count = 1000
movie_count = 10000
review_count = 50000

def main():
    random.seed(12345)
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")

    print("Adding users:", user_count)
    password_hash = generate_password_hash("salasana")
    users = [("kayttaja" + str(i), password_hash)
             for i in range(1, user_count + 1)]
    con.executemany(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)", users)

    print("Adding movies:", movie_count)
    movies = []
    for i in range(1, movie_count + 1):
        title = "Elokuva " + str(i)
        year = random.randint(1920, 2025)
        description = "Tämä on testidatana luotu elokuva, jolla ei ole " \
                      "varsinaista sisältöä. Tietueen numero on " + str(i) + "."
        user_id = random.randint(1, user_count)
        movies.append((title, year, description, user_id))
    con.executemany(
        """INSERT INTO movies (title, year, description, user_id)
           VALUES (?, ?, ?, ?)""", movies)

    print("Adding genres:", movie_count)
    movie_genres = set()
    for movie_id in range(1, movie_count + 1):
        for genre_id in random.sample(range(1, 11), random.randint(0, 3)):
            movie_genres.add((movie_id, genre_id))
    con.executemany(
        "INSERT INTO movie_genres (movie_id, genre_id) VALUES (?, ?)",
        movie_genres)

    print("Adding age ratings:", movie_count)
    movie_age_ratings = set()
    for movie_id in range(1, movie_count + 1):
        if random.random() < 0.5:
            age_rating_id = random.randint(1, 5)
            movie_age_ratings.add((movie_id, age_rating_id))
    con.executemany(
        """INSERT INTO movie_age_ratings (movie_id, age_rating_id)
           VALUES (?, ?)""", movie_age_ratings)

    print("Adding reviews:", review_count)
    reviews = []
    for i in range(1, review_count + 1):
        movie_id = random.randint(1, movie_count)
        user_id = random.randint(1, user_count)
        rating = random.randint(1, 10)
        comment = "Tämä on testidatana luotu arvostelu, jolla ei ole " \
                  "varsinaista sisältöä. Tietueen numero on " + str(i) + "."
        reviews.append((movie_id, user_id, rating, comment))
    con.executemany(
        """INSERT INTO reviews (movie_id, user_id, rating, comment)
           VALUES (?, ?, ?, ?)""", reviews)

    con.commit()
    con.close()
    print("Done")

if __name__ == "__main__":
    main()
