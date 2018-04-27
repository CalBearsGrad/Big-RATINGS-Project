"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Rating, Movie, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.

app.jinja_env.undefined = StrictUndefined
# app.jinja_env.undefined = jinja2.StrictUndefined


@app.route('/')
def index():
    """Homepage and registration form."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route('/check-user', methods=["POST", "GET"])
def check_user():
    """allow a new user to register email address and password
    """
    email = request.form.get("email")
    password = request.form.get("password")

    session['email'] = email
    session['password'] = password

    # print User.query.filter_by(email=email).first()

    print email
    print password

    reference_email = User.query.filter_by(email=email).first()

    # user_email = reference_email.email

    if reference_email:

        return render_template("log_in.html",
                               email=email,
                               password=password)
    else:
        return render_template("register.html",
                               email=email,
                               password=password)


@app.route('/register', methods=["POST"])
def register_user():
    """allow user to register email, password, age and zipcode
    """

    """defining the user input that we are getting """
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    email = session["email"]
    password = session["password"]

    """Instantiating a new user """
    user = User(email=email, password=password, age=age, zipcode=zipcode)
    print "I am email", email
    print "I am password", password
    print "I am age", age
    print "I am zipcode", zipcode
    db.session.add(user)
    db.session.commit()
    print "We created a new user!"

    flash("You have registered successfully")

    return render_template("log_in.html")


@app.route("/log_in", methods=["POST"])
def log_in():
    """allow user to log_in
    """

    email = request.form.get("email")
    password = request.form.get("password")

    if email in session and password in session:

        return render_template("homepageloggedin.html",
                               email=email,
                               password=password)
    else:
        return render_template("log_in.html")


@app.route("/homepageloggedin", methods=["POST"])
def logged_in():
    """renders the homepage when user is logged in.
    """

    email = request.form.get("email")
    password = request.form.get("password")

    print "Im inside /homepageloggedin"

    flash("You are logged in!")

    return render_template("homepageloggedin.html",
                           email=email,
                           password=password)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
