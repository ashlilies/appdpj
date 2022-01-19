from flask import url_for, render_template
from werkzeug.utils import redirect

from application import app

# <------------------------- ASHLEE ------------------------------>
# Old one - redirect to the new /consumer


@app.route('/')
@app.route('/home')
def home():
    # render a template
    # return render_template('home.html')
    return redirect(url_for("consumer_home"))


@app.route("/consumer")
def consumer_home():
    return render_template("consumer/home.html")


