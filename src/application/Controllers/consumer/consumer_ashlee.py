import functools

from flask import url_for, render_template, flash
from flask_login import current_user
from werkzeug.utils import redirect

from application import app
from application.Models.Admin import Admin
from application.Models.Consumer import Consumer


# <------------------------- ASHLEE ------------------------------>

# Decorator to only allow consumer accounts or guests
def consumer_side(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if isinstance(current_user, Consumer) or not current_user.is_authenticated:
            print(current_user)
            return view(*args, **kwargs)
        flash("You need to log out first to access the Consumer side.")
        return redirect('/admin')
    return wrapper


@app.route('/')
@app.route("/consumer", alias=True)
@consumer_side
def consumer_home():
    return render_template("consumer/home.html")


@app.route('/cart')
@consumer_side
def consumer_cart():
    return render_template("consumer/cart.html")

