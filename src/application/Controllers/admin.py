# Controller for the Admin side of things.
from flask import render_template

from application import app


@app.route("/admin")
@app.route("/admin/home")
def admin_home():
    return render_template("admin/home.html")


@app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html")


@app.route("/admin/register")
def admin_register():
    return render_template("admin/register.html")
