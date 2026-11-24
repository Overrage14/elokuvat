"""Movie database web application built with Flask and SQLite."""

import argparse
import secrets
import sqlite3
from functools import wraps
from urllib.parse import quote, urlsplit

from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
import markupsafe

import config
import db
import movies
import reviews
import users

app = Flask(__name__)
app.secret_key = config.secret_key

page_size = 10

@app.before_request
def prepare_session():
    """Ensure that the session has a CSRF token and a valid user."""
    if request.endpoint == "static":
        return
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    user_id = session.get("user_id")
    if user_id is not None and not users.get_user(user_id):
        session.clear()
        session["csrf_token"] = secrets.token_hex(16)

def get_page(item_count, page_param="page"):
    """Return the requested page number and the total number of pages."""
    page = request.args.get(page_param, "1")
    if not page.isdigit():
        abort(403)
    page = int(page)
    page_count = max(1, (item_count + page_size - 1) // page_size)
    if page < 1 or page > page_count:
        abort(404)
    return page, page_count

def get_local_referrer():
    """Return the local path of the referring page."""
    referrer = request.referrer
    if not referrer:
        return "/"
    parts = urlsplit(referrer)
    if parts.netloc and parts.netloc != request.host:
        return "/"
    path = parts.path or "/"
    if parts.query:
        path += "?" + parts.query
    return path

def redirect_to_login():
    """Redirect to login and remember the requested page."""
    flash("Kirjaudu sisään jatkaaksesi.", "info")
    next_page = request.path
    if request.method == "POST":
        next_page = get_local_referrer()
    return redirect("/login?next_page=" + quote(next_page))

def login_required(view):
    """Redirect to login if the user is not logged in."""
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        """Run the view if the user is logged in."""
        if "user_id" not in session:
            return redirect_to_login()
        return view(*args, **kwargs)
    return wrapped_view

def get_next_page(default="/"):
    """Return a safe local URL to redirect to after login."""
    next_page = request.values.get("next_page", default)
    if not next_page.startswith("/") or next_page.startswith("//"):
        return default
    if "\\" in next_page:
        return default
    if next_page in ("/login", "/register", "/create", "/logout"):
        return default
    return next_page

def check_csrf():
    """Abort the request if the CSRF token is missing or invalid."""
    token = request.form.get("csrf_token")
    if not token or token != session.get("csrf_token"):
        abort(403)

def flash_errors(errors):
    """Add all given error messages to the flash queue."""
    for error in errors:
        flash(error, "error")

@app.template_filter()
def show_lines(content):
    """Escape text and convert newlines to HTML line breaks."""
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

def render_movie_page(movie, filled_review=None):
    """Render a movie page with classifications and reviews."""
    genres = movies.get_genres(movie["id"])
    age_ratings = movies.get_age_ratings(movie["id"])
    movie_reviews = reviews.get_reviews(movie["id"])
    average_rating = reviews.get_average_rating(movie["id"])
    review_count = reviews.get_review_count(movie["id"])
    user_id = session.get("user_id")
    user_reviewed = any(review["user_id"] == user_id
                        for review in movie_reviews)
    return render_template("show_movie.html", movie=movie, genres=genres,
                           age_ratings=age_ratings, reviews=movie_reviews,
                           average_rating=average_rating,
                           review_count=review_count,
                           user_reviewed=user_reviewed,
                           filled_review=filled_review or {})

@app.route("/")
def index():
    """Show the front page with paginated movies."""
    movie_count = movies.get_movies_count()
    page, page_count = get_page(movie_count)
    all_movies = movies.get_movies(page, page_size)
    return render_template("index.html", movies=all_movies, page=page,
                           page_count=page_count, page_url="/?",
                           page_param="page", movie_count=movie_count)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    """Show a user's statistics and movies."""
    user = users.get_user(user_id)
    if not user:
        abort(404)
    movie_count = users.get_movie_count(user_id)
    page, page_count = get_page(movie_count)
    user_movies = users.get_movies(user_id, page, page_size)
    review_count = users.get_review_count(user_id)
    review_page, review_page_count = get_page(review_count, "review_page")
    user_reviews = users.get_reviewed_movies(user_id, review_page, page_size)
    base_url = "/user/" + str(user_id) + "?"
    return render_template("show_user.html", user=user, movies=user_movies,
                           reviews=user_reviews, movie_count=movie_count,
                           review_count=review_count, page=page,
                           page_count=page_count, page_param="page",
                           page_url=base_url + "review_page=" +
                           str(review_page) + "&",
                           review_page=review_page,
                           review_page_count=review_page_count,
                           review_page_url=base_url + "page=" +
                           str(page) + "&")

@app.route("/find_movie")
def find_movie():
    """Search movies by keyword and genre."""
    query = request.args.get("query", "").strip()
    genre_id = request.args.get("genre_id", "").strip()
    genres = movies.get_all_genres()
    results = []
    movie_count = 0
    page = None
    page_count = None
    page_url = "/find_movie?"

    if len(query) > 100:
        flash("VIRHE: hakusana voi olla enintään 100 merkkiä", "error")
        query = ""

    if query or genre_id:
        if genre_id:
            valid_ids = {genre["id"] for genre in genres}
            if not genre_id.isdigit() or int(genre_id) not in valid_ids:
                abort(403)
            genre_id = int(genre_id)
        movie_count = movies.find_movies_count(query, genre_id)
        page, page_count = get_page(movie_count)
        results = movies.find_movies(query, genre_id, page, page_size)
        if query:
            page_url += "query=" + quote(query) + "&"
        if genre_id:
            page_url += "genre_id=" + str(genre_id) + "&"
    return render_template("find_movie.html", query=query, results=results,
                           genres=genres, genre_id=genre_id, page=page,
                           page_count=page_count, page_url=page_url,
                           page_param="page", movie_count=movie_count)

@app.route("/movie/<int:movie_id>")
def show_movie(movie_id):
    """Show a single movie."""
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    return render_movie_page(movie)

@app.route("/new_movie")
@login_required
def new_movie():
    """Show the form for adding a new movie."""
    genres = movies.get_all_genres()
    age_ratings = movies.get_all_age_ratings()
    return render_template("new_movie.html", genres=genres,
                           age_ratings=age_ratings, filled={},
                           genre_ids=[], age_rating_id=None)

@app.route("/create_movie", methods=["POST"])
@login_required
def create_movie():
    """Create a new movie from the submitted form."""
    check_csrf()

    title, year, description, errors = movies.validate_movie_data(
        request.form)
    genre_ids = movies.get_selected_genres(request.form)
    age_rating_id = movies.get_selected_age_rating(request.form)

    if errors:
        flash_errors(errors)
        return render_template("new_movie.html",
                               genres=movies.get_all_genres(),
                               age_ratings=movies.get_all_age_ratings(),
                               filled={"title": title, "year": year,
                                       "description": description},
                               genre_ids=genre_ids,
                               age_rating_id=age_rating_id)

    movie_id = movies.add_movie(title, int(year), description,
                                session["user_id"], genre_ids, age_rating_id)
    flash("Elokuvan lisääminen onnistui", "success")
    return redirect("/movie/" + str(movie_id))

@app.route("/edit_movie/<int:movie_id>")
@login_required
def edit_movie(movie_id):
    """Show the form for editing an existing movie."""
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
    filled = {"title": movie["title"], "year": movie["year"],
              "description": movie["description"]}

    return render_template("edit_movie.html", movie=movie, genres=all_genres,
                           age_ratings=all_age_ratings, genre_ids=genre_ids,
                           age_rating_id=age_rating_id, filled=filled)

@app.route("/update_movie", methods=["POST"])
@login_required
def update_movie():
    """Update an existing movie from the submitted form."""
    check_csrf()

    movie = movies.get_movie(request.form.get("movie_id", ""))
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    title, year, description, errors = movies.validate_movie_data(
        request.form)
    genre_ids = movies.get_selected_genres(request.form)
    age_rating_id = movies.get_selected_age_rating(request.form)

    if errors:
        flash_errors(errors)
        return render_template("edit_movie.html", movie=movie,
                               genres=movies.get_all_genres(),
                               age_ratings=movies.get_all_age_ratings(),
                               filled={"title": title, "year": year,
                                       "description": description},
                               genre_ids=genre_ids,
                               age_rating_id=age_rating_id)

    movies.update_movie(movie["id"], title, int(year), description,
                        genre_ids, age_rating_id)
    flash("Elokuvan muokkaaminen onnistui", "success")
    return redirect("/movie/" + str(movie["id"]))

@app.route("/remove_movie/<int:movie_id>", methods=["GET", "POST"])
@login_required
def remove_movie(movie_id):
    """Show the removal confirmation or remove a movie."""
    movie = movies.get_movie(movie_id)
    if not movie:
        abort(404)
    if movie["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_movie.html", movie=movie)

    check_csrf()
    if "remove" in request.form:
        movies.remove_movie(movie_id)
        flash("Elokuvan poistaminen onnistui", "success")
        return redirect("/")
    return redirect("/movie/" + str(movie_id))

@app.route("/create_review", methods=["POST"])
@login_required
def create_review():
    """Create a review for a movie."""
    check_csrf()

    movie = movies.get_movie(request.form.get("movie_id", ""))
    if not movie:
        abort(403)

    rating, comment, errors = reviews.validate_review_data(
        request.form)
    filled_review = {"rating": rating, "comment": comment}
    if errors:
        flash_errors(errors)
        return render_movie_page(movie, filled_review)

    try:
        reviews.add_review(movie["id"], session["user_id"], int(rating),
                           comment)
    except sqlite3.IntegrityError:
        flash("VIRHE: olet jo antanut arvostelun tälle elokuvalle", "error")
        return render_movie_page(movie, filled_review)

    flash("Arvostelun lähettäminen onnistui", "success")
    return redirect("/movie/" + str(movie["id"]))

@app.route("/edit_review/<int:review_id>")
@login_required
def edit_review(review_id):
    """Show the form for editing an existing review."""
    review = reviews.get_review(review_id)
    if not review:
        abort(404)
    if review["user_id"] != session["user_id"]:
        abort(403)
    filled = {"rating": review["rating"], "comment": review["comment"]}
    return render_template("edit_review.html", review=review, filled=filled)

@app.route("/update_review", methods=["POST"])
@login_required
def update_review():
    """Update an existing review from the submitted form."""
    check_csrf()

    review = reviews.get_review(request.form.get("review_id", ""))
    if not review:
        abort(404)
    if review["user_id"] != session["user_id"]:
        abort(403)

    rating, comment, errors = reviews.validate_review_data(
        request.form)
    filled = {"rating": rating, "comment": comment}

    if errors:
        flash_errors(errors)
        return render_template("edit_review.html", review=review,
                               filled=filled)

    reviews.update_review(review["id"], int(rating), comment)
    flash("Arvostelun muokkaaminen onnistui", "success")
    return redirect("/movie/" + str(review["movie_id"]))

@app.route("/remove_review/<int:review_id>", methods=["GET", "POST"])
@login_required
def remove_review(review_id):
    """Show the removal confirmation or remove a review."""
    review = reviews.get_review(review_id)
    if not review:
        abort(404)
    if review["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_review.html", review=review)

    check_csrf()
    if "remove" in request.form:
        reviews.remove_review(review_id)
        flash("Arvostelun poistaminen onnistui", "success")
        return redirect("/movie/" + str(review["movie_id"]))
    return redirect("/movie/" + str(review["movie_id"]))

@app.route("/register")
def register():
    """Show the registration form."""
    return render_template("register.html", filled={})

@app.route("/create", methods=["POST"])
def create():
    """Create a new user account."""
    check_csrf()

    username = request.form.get("username", "").strip()
    password1 = request.form.get("password1", "")
    password2 = request.form.get("password2", "")
    errors = []

    if not username:
        errors.append("VIRHE: lisää tunnus")
    elif len(username) > 30:
        errors.append("VIRHE: tunnus voi olla enintään 30 merkkiä")

    if not password1.strip():
        errors.append("VIRHE: lisää salasana")
    elif len(password1) > 100:
        errors.append("VIRHE: salasana voi olla enintään 100 merkkiä")

    if not password2.strip():
        errors.append("VIRHE: toista salasana")

    if password1 != password2:
        errors.append("VIRHE: salasanat eivät ole samat")

    if errors:
        flash_errors(errors)
        return render_template("register.html", filled={"username": username})

    try:
        user_id = users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu", "error")
        return render_template("register.html", filled={"username": username})

    session["user_id"] = user_id
    session["username"] = username
    session["csrf_token"] = secrets.token_hex(16)
    flash("Tunnuksen luominen onnistui", "success")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Show the login form or log the user in."""
    next_page = get_next_page()

    if request.method == "GET":
        return render_template("login.html", filled={},
                               next_page=next_page)

    check_csrf()

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    errors = []

    if not username:
        errors.append("VIRHE: lisää tunnus")
    if not password:
        errors.append("VIRHE: lisää salasana")

    if errors:
        flash_errors(errors)
        return render_template("login.html",
                               filled={"username": username},
                               next_page=next_page)

    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect(next_page)
    flash("VIRHE: väärä tunnus tai salasana", "error")
    return render_template("login.html", filled={"username": username},
                           next_page=next_page)

@app.route("/logout")
def logout():
    """Log the user out and clear the session."""
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--time-db", action="store_true",
                        help="print the duration of each database operation")
    arguments = parser.parse_args()
    if arguments.time_db:
        db.time_queries = True
    app.run()
