# Controller for the Admin side of things.
from flask import render_template

from application import app


@app.route("/admin")
@app.route("/admin/home")
def admin_home():
    return render_template("admin/home.html")
