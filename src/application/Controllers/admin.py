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


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():  # ashlee
    def login_error():
        return redirect("%s?error=1" % url_for("admin_login"))

    if request.method == "POST":
        # That means user submitted login form. Check errors.
        login = Account.login_user(request.form["email"],
                                   request.form["password"])
        if login is not None:
            # user entered correct credentials
            # TODO Link dashboard or something from here
            session["account_id"] = login.account_id
            return redirect(url_for("admin_home"))
        return login_error()
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
        session["account_id"] = account.account_id
        return redirect(url_for("admin_home"))

    return render_template("admin/register.html")


@app.route("/admin/logout")
def admin_logout():
    try:
        logging.info("Admin %s logged out"
                     % gabi(session["account_id"]).get_email())
        del session["account_id"]
    except (NameError, AttributeError) as e:
        logging.info("admin_logout(): Failed logout - lag or click twice (%s)"
                     % e)
        pass  # user already logged out; lag or clicked twice

    return redirect(url_for("admin_home"))


# IAIIS
def is_account_id_in_session():  # for flask
    if "account_id" in session:
        # account value exists in session, check if admin account active
        if Admin.check_active(gabi(session["account_id"])) is not None:
            logging.info("IAIIS: Account id of %s is active and inside session" % session["account_id"])
            return gabi(session["account_id"])
    else:
        logging.info("IAIIS: Account id is NOT inside session or disabled")
    return None


# Get account by ID
def gabi(account_id):  # for flask
    return Account.get_account_by_id(account_id)


# Get ADMIN account by ID
# def gaabi(account_id):  # for our internal use to make other Flask functions
#     return Admin.get_account_by_id(account_id)


def get_restaurant_name_by_id(id):
    restaurant_account = gabi(id)
    rname = restaurant_account.restaurant_name
    return rname


# TODO; store Flask session info in shelve db

# Activate global function for jinja
app.jinja_env.globals.update(is_account_id_in_session=is_account_id_in_session)
# app.jinja_env.globals.update(gabi=gabi)
app.jinja_env.globals.update(get_restaurant_name_by_id=get_restaurant_name_by_id)


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
