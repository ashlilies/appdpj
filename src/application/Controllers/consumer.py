# Controller for the Consumer side of things.
# Do NOT run directly. Run main.py in the appdpj/src/ directory instead.

# New routes go here, not in __init__.

# Fill your @app.routes below here...
from flask import render_template, redirect, url_for

from application import app


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
