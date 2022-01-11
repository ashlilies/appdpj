# Controller for the Admin side of things.
# Do NOT run directly. Run main.py in the appdpj/src/ directory instead.

# New routes go here, not in __init__.

from flask import render_template, request, redirect, url_for, session, flash
from application.Models.Admin import *
from application.Models.Food import Food
from application.Models.Restaurant import Restaurant
from application import app, DB_NAME
from application.Models.Transaction import Transaction
from application.adminAddFoodForm import CreateFoodForm
from werkzeug.utils import secure_filename

from application.restaurantCertification import RestaurantCertification
import shelve, os
from application.rest_details_form import RestaurantDetailsForm


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
                logging.info("admin_register: error %s" % e)
                return reg_error(e)  # handle errors here
        else:
            return reg_error()

        # Successfully registered
        # TODO: Link dashboard or something
        # TODO: Set flask session
        session["account_id"] = account.account_id
        return redirect(url_for("create"))

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
        if request.form["changeEmail"] != "":
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
        elif request.form["changePw"] != "":
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


def get_restaurant_name_by_id(restaurant_id):
    restaurant_account = gabi(restaurant_id)
    return getattr(restaurant_account, "restaurant_name", None)


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
    with shelve.open(DB_NAME, 'c') as db:
        if "food" in db:
            food_list = db['food']
        else:
            food_list = []
            db["food"] = food_list

    return render_template('admin/foodManagement.html',
                           food_list=food_list)


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


# <------------------------- YONG LIN ------------------------------>
@app.route("/admin/transaction/createExampleTransactions")
def create_example_transactions():
    # WARNING - Overrides ALL transactions in the db!
    transaction_list = []

    # creating a shelve file with dummy data
    # 1: <account id> ; <user_id> ; <option> ; <price> ; <coupons> , <rating>
    t1 = Transaction()
    t1.account_name = 'Yong Lin'
    t1.set_option('Delivery')
    t1.set_price(50.30)
    t1.set_used_coupons('SPAGETIT')
    t1.set_ratings(2)
    transaction_list.append(t1)

    t2 = Transaction()
    t2.account_name = 'Ching Chong'
    t2.set_option('Dine-in')
    t2.set_price(80.90)
    t2.set_used_coupons('50PASTA')
    t2.set_ratings(5)
    transaction_list.append(t2)

    t3 = Transaction()
    t3.account_name = 'Hosea'
    t3.set_option('Delivery')
    t3.set_price(20.10)
    t3.set_used_coupons('50PASTA')
    t3.set_ratings(1)
    transaction_list.append(t3)

    t4 = Transaction()
    t4.account_name = 'Clara'
    t4.set_option('Delivery')
    t4.set_price(58.30)
    t4.set_used_coupons('SPAGETIT')
    t4.set_ratings(2)
    transaction_list.append(t4)

    t5 = Transaction()
    t5.account_name = 'Ruri'
    t5.set_option('Dine-in')
    t5.set_price(80.90)
    t5.set_used_coupons('50PASTA')
    t5.set_ratings(3)
    transaction_list.append(t5)

    t6 = Transaction()  # t6
    t6.account_name = 'Ashlee'
    t6.set_option('Delivery')
    t6.set_price(100.10)
    t6.set_used_coupons('50PASTA')
    t6.set_ratings(2)
    transaction_list.append(t6)

    t7 = Transaction()
    t7.account_name = 'Hello'
    t7.set_option('Dine-in')
    t7.set_price(10.90)
    t7.set_used_coupons('50PASTA')
    t7.set_ratings(4)
    transaction_list.append(t7)

    # writing to the database
    with shelve.open(DB_NAME, "c") as db:
        try:
            db['shop_transactions'] = transaction_list
        except Exception as e:
            logging.error("create_example_transactions: error writing to db (%s)" % e)

    return redirect(url_for("admin_transaction"))


@app.route("/admin/transaction")
def admin_transaction():
    # read transactions from db
    with shelve.open(DB_NAME, 'c') as db:
        if 'shop_transactions' in db:
            transaction_list = db['shop_transactions']
            logging.info("admin_transaction: reading from db['shop_transactions']"
                         ", %d elems" % len(db["shop_transactions"]))
        else:
            logging.info("admin_transaction: nothing found in db, starting empty")
            transaction_list = []

    def get_transaction_by_id(transaction_id):  # debug
        for transaction in transaction_list:
            if transaction_id == transaction.count_id:
                return transaction

    return render_template("admin/transaction.html", count=len(transaction_list),
                           transaction_list=transaction_list)


# soft delete -> restaurant can soft delete transactions jic if the transaction is cancelled
# set instance attribute of Transaction.py = False
@app.route('/admin/transaction/delete/<transaction_id>')
def delete_transaction(transaction_id):
    transaction_id = int(transaction_id)

    transaction_list = []
    # TODO: SOFT DELETE TRANSACTIONS -> set instance attribute to False
    with shelve.open(DB_NAME, 'c') as db:
        for transaction in db['shop_transactions']:
            transaction_list.append(transaction)

    def get_transaction_by_id(t_id):  # debug
        for t in transaction_list:
            if t_id == t.count_id:
                return t

    logging.info("delete_transaction: deleted transaction with id %d"
                 % transaction_id)
    get_transaction_by_id(transaction_id).deleted = True
    with shelve.open(DB_NAME, 'c') as db:
        db["shop_transactions"] = transaction_list

    return redirect(url_for('admin_transaction'))


# certification -- xu yong lin
# UPLOAD_FOLDER = 'application/static/restaurantCertification'  # where the
# files are stored to
# ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
#
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in
#     ALLOWED_EXTENSIONS
path = os.getcwd()

UPLOAD_CERT = os.path.join(path, 'uploads')

app.config['UPLOAD_CERT'] = UPLOAD_CERT


@app.route("/admin/certification", methods=['GET', 'POST'])
def admin_certification():
    # set upload directory path
    certification_form = RestaurantCertification()
    if certification_form.validate_on_submit():
        # assets_dir = os.path.join(
        #     os.path.dirname(app.instance_path), 'assets'
        # )
        hygiene = certification_form.hygiene_cert.data
        halal = certification_form.halal_cert.data
        vegetarian = certification_form.vegetarian_cert.data
        vegan = certification_form.vegan_cert.data

        halaldoc_name = secure_filename(halal.filename)
        vegetariandoc_name = secure_filename(vegetarian.filename)
        vegandoc_name = secure_filename(vegan.filename)

        # document save
        # halal.save(os.path.join(app.config['UPLOAD_FOLDER'], halaldoc_name))
        # TODO: SAVING OF FILE
        # TODO: DISPLAYING OF AVAILABLE FILES UNDER myrestaurant
        # todo: updating of cert under myrestaurant

        # halal.save(os.path.join('/application/static/restaurantCertification', halaldoc_name))
        # vegetarian.save(
        #     os.path.join('/application/static/restaurantCertification', vegetariandoc_name))
        # vegan.save(os.path.join('/application/static/restaurantCertification', vegandoc_name))

        flash('Document uploaded successfully')

        # return redirect(url_for('admin_myrestaurant'))

    return render_template("admin/certification.html",
                           certification_form=certification_form)


# <------------------------- RURI ------------------------------>
@app.route('/admin/myRestaurant', methods=['GET', 'POST'])
def admin_myrestaurant():  # ruri
    restaurant_details_form = RestaurantDetailsForm(request.form)
    restaurants_dict = {}
    if request.method == 'POST' and restaurant_details_form.validate():
        db = shelve.open(DB_NAME, 'c')
        try:
            restaurants_dict = db['Restaurants']
        except Exception as e:
            logging.error("Error in retrieving Restaurants from "
                          "restaurants.db (%s)" % e)

        restaurant = Restaurant(restaurant_details_form.rest_name.data)
        restaurants_dict[restaurant.name] = restaurant
        db['Restaurants'] = restaurants_dict

        db.close()

    return render_template("admin/restaurant.html", form=restaurant_details_form)


# #
# @app.route('admin/myrestaurant', methods=['GET', 'POST'])
# def create_customer():
#     create_customer_form: CreateCustomerForm = CreateCustomerForm(request.form)
#     if request.method == 'POST' and create_customer_form.validate():
#         customers_dict = {}
#         db = shelve.open('customer.db', 'c')
#
#         try:
#             customers_dict = db['Customers']
#         except:
#             print("Error in retrieving Customers from customer.db.")
#
#         customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
#                                      create_customer_form.gender.data, create_customer_form.membership.data,
#                                      create_customer_form.remarks.data, create_customer_form.email.data,
#                                      create_customer_form.date_joined.data,
#                                      create_customer_form.address.data, )
#         customers_dict[customer.get_customer_id()] = customer
#         db['Customers'] = customers_dict
#
#         db.close()
#
#         return redirect(url_for('home'))
#     return render_template('includes/createCustomer.html', form=create_customer_form)


@app.route("/admin/dashboard")
def dashboard():  # ruri
    return render_template("admin/dashboard.html")

