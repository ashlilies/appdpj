# Controller for the Admin side of things.
from flask import render_template, session

from flask import Flask, render_template, request, redirect, url_for
from application.Models.Admin import *
from application import app


@app.route("/admin")
@app.route("/admin/home")
def admin_home():
    return render_template("admin/home.html")


@app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html")


@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():
    def reg_error():
        return redirect("%s?error=1" % url_for("admin_register"))

    if request.method == "POST":
        # Check for errors in the form submitted
        if (request.form["tosAgree"] == "agreed"
                and request.form["password"] == request.form["passwordAgain"]):
            try:
                account = Admin(request.form["name"], request.form["email"],
                                request.form["password"])
            except Exception as e:
                return reg_error()  # handle errors here
        else:
            return reg_error()

        # Successfully registered
        # TODO: Link dashboard or something
        # TODO: Set flask session
        session["account"] = account.account_id
        return redirect(url_for("admin_home"))

    return render_template("admin/register.html")


@app.route("/admin/transaction")
def admin_transaction():
    # users_dict = {}
    # db = shelve.open('user.db', 'r')
    # users_dict = db['Users']
    # db.close()
    # users_list = []
    # for key in users_dict:
    #     user = users_dict.get(key)
    #     users_list.append(user)
    return render_template('admin/transaction.html', count=len(users_list), users_list=users_list)
