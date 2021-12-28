# Controller for the Admin side of things.
# Do NOT run directly. Run main.py in the appdpj/src/ directory instead.

# New routes go here, not in __init__.

from flask import render_template, request, redirect, url_for, session, flash
from application.Models.Admin import *
from application.Models.Food import Food
from application import app
from application.adminAddFoodForm import CreateFoodForm
import shelve, os


# <------------------------- ASHLEE ------------------------------>
@app.route("/admin")
@app.route("/admin/home")
def admin_home():  # ashlee
    return render_template("admin/home.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():  # ashlee
    # if already logged in, what's the point?
    if is_account_id_in_session():
        return redirect(url_for("admin_home"))

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
    # if already logged in, what's the point?
    if is_account_id_in_session():
        return redirect(url_for("admin_home"))

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
    if "account_id" in session:
        logging.info("admin_logout(): Admin %s logged out"
                     % gabi(session["account_id"]).get_email())
        del session["account_id"]
    else:
        logging.info("admin_logout(): Failed logout - lag or click twice")

    return redirect(url_for("admin_home"))


# API for updating account, to be called by Account Settings
@app.route("/admin/updateAccount", methods=["GET", "POST"])
def admin_update_account():
    # TODO: Implement admin account soft-deletion
    #       and update restaurant name

    if request.method == "GET":
        return "fail"
    if not is_account_id_in_session():
        return "fail"

    # Check if current password entered was correct
    if not is_account_id_in_session() \
            .check_password_hash(request.form["updateSettingsPw"]):
        return "Current Password is Wrong"

    response = ""
    if "changeEmail" in request.form:
        if request.form["changeEmail"] is not "":
            result = (is_account_id_in_session()
                      .set_email(request.form["changeEmail"]))
            if result == Account.EMAIL_CHANGE_SUCCESS:
                response = ("%sSuccessfully updated email<br>" % response)
            elif result == Account.EMAIL_CHANGE_ALREADY_EXISTS:
                response = ("%sFailed updating email, Email already Exists<br>"
                            % response)
            elif result == Account.EMAIL_CHANGE_INVALID:
                response = ("%sFailed updating email, email is Invalid<br>"
                            % response)

    if "changePw" in request.form:
        if request.form["changePw"] != request.form["changePwConfirm"]:
            response = ("%sConfirm Password does not match Password<br>"
                        % response)
        elif request.form["changePw"] is not "":
            is_account_id_in_session() \
                .set_password_hash(request.form["changePw"])
            response = "%sSuccessfully updated Password<br>" % response

    return response


# IAIIS - is logged in?
def is_account_id_in_session() -> Account or None:  # for flask
    if "account_id" in session:
        # account value exists in session, check if admin account active
        if Admin.check_active(gabi(session["account_id"])) is not None:
            logging.info(
                "IAIIS: Account id of %s is active and inside session" %
                session["account_id"])
            return gabi(session["account_id"])
    else:
        logging.info("IAIIS: Account id is NOT inside session or disabled")
    return None


# Get account by ID
def gabi(account_id) -> Account:  # for flask
    return Account.get_account_by_id(account_id)


# Get ADMIN account by ID
# def gaabi(account_id):  # for our internal use to make other Flask functions
#     return Admin.get_account_by_id(account_id)


def get_restaurant_name_by_id(id):
    restaurant_account = gabi(id)
    rname = restaurant_account.restaurant_name
    return rname


# Used for the Account Settings pane.
def get_account_email(account: Account):
    try:
        return account.get_email()
    except Exception as e:
        logging.info(e)
        return "ERROR"

# TODO; store Flask session info in shelve db

# Activate global function for jinja
app.jinja_env.globals.update(is_account_id_in_session=is_account_id_in_session)
# app.jinja_env.globals.update(gabi=gabi)
app.jinja_env.globals.update(
    get_restaurant_name_by_id=get_restaurant_name_by_id)
app.jinja_env.globals.update(get_account_email=get_account_email)


# <------------------------- CLARA ------------------------------>
# APP ROUTE TO FOOD MANAGEMENT clara
@app.route("/admin/foodManagement")
def food_management():
    return render_template('admin/foodManagement.html')


MAX_SPECIFICATION_ID = 5  # for adding food
MAX_TOPPING_ID = 8


# ADMIN FOOD FORM clara
@app.route('/admin/addFoodForm', methods=['GET', 'POST'])
def create_food():
    create_food_form = CreateFoodForm(request.form)

    # get specifications as a List, no WTForms
    def get_specs() -> list:
        specs = []

        # do specifications exist in first place?
        for i in range(MAX_SPECIFICATION_ID + 1):
            if "specification%d" % i in request.form:
                specs.append(request.form["specification%d" % i])
            else:
                break

        logging.info("create_food: specs is %s" % specs)
        return specs

        # get toppings as a List, no WTForms

    def get_top() -> list:
        top = []

        # do toppings exist in first place?
        for i in range(MAX_TOPPING_ID + 1):
            if "topping%d" % i in request.form:
                top.append(request.form["topping%d" % i])
            else:
                break

        logging.info("create_food: top is %s" % top)
        return top

    # using the WTForms way to get the data
    if request.method == 'POST' and create_food_form.validate():
        food_list = []
        with shelve.open("foodypulse", "c") as db:
            try:
                if 'food' in db:
                    food_list = db['food']
                else:
                    db['food'] = food_list
            except Exception as e:
                logging.error("create_food: error opening db (%s)" % e)

        # Create a new food object
        food = Food(request.form["image"], create_food_form.item_name.data,
                    create_food_form.description.data,
                    create_food_form.price.data, create_food_form.allergy.data)

        food.specification = get_specs()  # set specifications as a List
        food.topping = get_top()  # set topping as a List
        food_list.append(food)

        # writeback
        with shelve.open("foodypulse", 'c') as db:
            db['food'] = food_list

        return redirect(url_for('admin_home'))

    return render_template('admin/addFoodForm.html', form=create_food_form,
                           MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                           MAX_TOPPING_ID=MAX_TOPPING_ID, )


# <------------------------- YONGLIN ------------------------------>
@app.route("/admin/transaction")
def admin_transaction():
    return render_template("admin/transaction.html")


# certification -- xu yong lin
UPLOAD_FOLDER = 'application/static/restaurantCertification'  # where the files are stored to
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/admin/certification", methods=['GET', 'POST'])
def admin_certification():
    if request.method == "POST":
        # check if the post request has file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('admin_myrestaurant'))
        restaurantFile = request.files['file']

        # if user did not select a file, the browser submits an empty file w/o a filename
        if restaurantFile.filename == '':
            flash('No selected file')
            return redirect(url_for('admin_certification'))
        if restaurantFile and allowed_file(restaurantFile.filename):
            restaurantFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))

    return render_template("admin/certification.html")


# <------------------------- RURI ------------------------------>
@app.route("/admin/myRestaurant")
def admin_myrestaurant():  # ruri
    return render_template("admin/restaurant.html")

@app.route("/admin/tags")
def admin_tags():  # ruri
    return render_template("admin/tags.html")
