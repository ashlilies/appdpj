from flask import url_for, render_template
from werkzeug.utils import redirect

from application import app


# <------------------------- ASHLEE ------------------------------>
@app.route('/')
@app.route("/consumer", alias=True)
def consumer_home():
    return render_template("consumer/home.html")


@app.route('/cart')
def consumer_cart():
    return render_template("consumer/cart.html")

