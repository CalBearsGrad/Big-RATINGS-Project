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
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)

@app.route('/check-user', methods=["GET"])
def check_user(email):
    """allow a new user to register email address and password
    """
    email = request.form.get("email")
    password = request.form.get("password")

    print email
    print password

    if email == User.query.filter_by(email=email).first():
        return render_template("log_in.html",
                               email=email,
                               password=password)
    else:
        return render_template("registration.html",
                               email=email,
                               password=password)


@app.route('/registration', methods=["POST"])
def register_user():
    """allow user to register email, password, age and zipcode
    """

    """defining the user input that we are getting """
    age = request.forms.get("age")
    zipcode = request.forms.get("zipcode")
    email = request.args.get("email")
    password = request.args.get("password")

    """Instantiating a new user """
    age = User.age
    zipcode = User.zipcode
    email = User.email
    password = User.password

    flash("You have registered in successfully")

    return render_template("log_in.html")

@app.route("/log_in", methods=["POST"])
def log_in():
    """allow user to log_in
    """



    return render_template("log_in.html")




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
