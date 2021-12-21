# Controller for the Admin side of things.

from flask import render_template, request, redirect, url_for, session
from application.Models.Admin import *
from application import app
from application.adminAddFoodForm import CreateFoodForm


# <------------------------- ASHLEE ------------------------------>
@app.route("/admin")
@app.route("/admin/home")
def admin_home():  # ashlee
    return render_template("admin/home.html")


@app.route("/admin/login")
def admin_login():  # ashlee
    return render_template("admin/login.html")


@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():  # ashlee
    def reg_error(ex=None):
        if ex is not None:
            if Account.EMAIL_ALREADY_EXISTS in ex.args:
                return redirect("%s?emailExists=1" % url_for("admin_register"))
        # Given js validation, shouldn't reach here by a normal user.
        return redirect("%s?error=1" % url_for("admin_register"))

    if request.method == "POST":
        # Check for errors in the form submitted
        if (request.form["tosAgree"] == "agreed"
                and request.form["email"] != ""  # not blank email
                and request.form["name"] != ""  # not blank restaurant name
                and request.form["password"] != ""  # not blank pw
                and request.form["password"] == request.form["passwordAgain"]):
            try:
                account = Admin(request.form["name"], request.form["email"],
                                request.form["password"])
            except Exception as e:
                return reg_error(e)  # handle errors here
        else:
            return reg_error()

        # Successfully registered
        # TODO: Link dashboard or something
        # TODO: Set flask session
        session["account"] = account.account_id
        return redirect(url_for("admin_home"))

    return render_template("admin/register.html")


# <------------------------- CLARA ------------------------------>
# APP ROUTE TO FOOD MANAGEMENT clara
@app.route("/admin/foodManagement")
def food_management():
    return render_template('admin/foodManagement.html')


# ADMIN FOOD FORM clara
@app.route('/admin/addFoodForm', methods=['GET', 'POST'])
def create_food():
    create_food_form = CreateFoodForm(request.form)
    if request.method == 'POST' and create_food_form.validate():
        return redirect(url_for('admin_home'))
    return render_template('admin/addFoodForm.html', form=create_food_form)


# <------------------------- YONGLIN ------------------------------>
@app.route("/admin/transaction")
def admin_transaction():   # yonglin
    return render_template("admin/transaction.html")


# <------------------------- RURI ------------------------------>
@app.route("/admin/myRestaurant")
def admin_myrestaurant():  # ruri
    return render_template("admin/restaurant.html")
