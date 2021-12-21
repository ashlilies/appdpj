# Controller for the Admin side of things.
from flask import render_template, session

from flask import Flask, render_template, request, redirect, url_for
from application.Models.Admin import *
from application import app
from application.Models.Logger import Logger


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

    # Set up a logger
    from application.Models.Logger import Logger
    logger = Logger("Registration")

    if request.method == "POST":
        # Check for errors in the form submitted
        if (request.form["tosAgree"] == "agreed"
                and request.form["password"] == request.form["passwordAgain"]):
            try:
                account = Admin(request.form["name"], request.form["email"],
                                request.form["password"])
            except Exception as e:
                logger.warn("Account creation error in initialization")
                return reg_error()  # handle errors here
        else:
            logger.warn("Account creation error - "
                        "User didn't agree to ToS or password mismatch")
            return reg_error()

        # Successfully registered
        # TODO: Link dashboard or something
        # TODO: Set flask session
        logger.info("Account created successfully")
        session["account"] = account.account_id
        return redirect(url_for("admin_home"))

    return render_template("admin/register.html")


@app.route("/admin/transaction")
def admin_transaction():
    return render_template("admin/transaction.html")
