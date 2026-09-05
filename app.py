import re
import secrets
import sqlite3

from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
import markupsafe

import config
import movies
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

def validate_movie_data():
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    year = request.form["year"]
    if not re.search("^[0-9]{4}$", year):
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    return title, int(year), description

def get_selected_genres():
    valid_ids = {genre["id"] for genre in movies.get_all_genres()}
    genre_ids = []
    for entry in request.form.getlist("genres"):
        if entry:
            if not entry.isdigit() or int(entry) not in valid_ids:
                abort(403)
            genre_ids.append(int(entry))
    return genre_ids

def get_selected_age_rating():
    valid_ids = {age_rating["id"] for age_rating in movies.get_all_age_ratings()}
    entry = request.form["age_rating"]
    if not entry:
        return None
    if not entry.isdigit() or int(entry) not in valid_ids:
        abort(403)
    return int(entry)

@app.route("/")
def index():
    all_movies = movies.get_movies()
    return render_template("index.html", movies=all_movies)

@app.route("/movie/<int:movie_id>")
def show_movie(movie_id):
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    genres = movies.get_genres(movie_id)
    age_ratings = movies.get_age_ratings(movie_id)
    return render_template("show_movie.html", movie=movie, genres=genres,
                           age_ratings=age_ratings)

@app.route("/new_movie")
def new_movie():
    require_login()
    genres = movies.get_all_genres()
    age_ratings = movies.get_all_age_ratings()
    return render_template("new_movie.html", genres=genres, age_ratings=age_ratings)

@app.route("/create_movie", methods=["POST"])
def create_movie():
    require_login()
    check_csrf()

    title, year, description = validate_movie_data()
    genre_ids = get_selected_genres()
    age_rating_id = get_selected_age_rating()

    movie_id = movies.add_movie(title, year, description,
                                session["user_id"], genre_ids, age_rating_id)
    return redirect("/movie/" + str(movie_id))

@app.route("/edit_movie/<int:movie_id>")
def edit_movie(movie_id):
    require_login()
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    all_genres = movies.get_all_genres()
    all_age_ratings = movies.get_all_age_ratings()
    genre_ids = [genre["id"] for genre in movies.get_genres(movie_id)]
    age_ratings = movies.get_age_ratings(movie_id)
    age_rating_id = age_ratings[0]["id"] if age_ratings else None

    return render_template("edit_movie.html", movie=movie, genres=all_genres,
                           age_ratings=all_age_ratings, genre_ids=genre_ids,
                           age_rating_id=age_rating_id)

@app.route("/update_movie", methods=["POST"])
def update_movie():
    require_login()
    check_csrf()

    movie_id = request.form["movie_id"]
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    title, year, description = validate_movie_data()
    genre_ids = get_selected_genres()
    age_rating_id = get_selected_age_rating()

    movies.update_movie(movie_id, title, year, description,
                        genre_ids, age_rating_id)
    return redirect("/movie/" + str(movie_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not username or len(username) > 30:
        abort(403)
    if not password1 or len(password1) > 100:
        abort(403)
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        flash("VIRHE: väärä tunnus tai salasana")
        return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
