# Controller for the Admin side of things.
# Do NOT run directly. Run main.py in the appdpj/src/ directory instead.

# New routes go here, not in __init__.
import traceback

from flask import render_template, request, redirect, url_for, session, flash, Flask
from flask_login import logout_user

from application.Models.Admin import *
from application.Models.Food import Food
from application.Models.Restaurant import Restaurant
from application import app, DB_NAME, login_manager
from application.Models.Transaction import Transaction
from application.adminAddFoodForm import CreateFoodForm
from werkzeug.utils import secure_filename
from application.Controllers.restaurant_controller import *
from application.restaurantCertification import RestaurantCertification
import shelve, os
import uuid
from application.rest_details_form import *


# <------------------------- ASHLEE ------------------------------>
# Our Login Manager
@login_manager.user_loader
def load_user(user_id):
    return Account.get_account_by_id(user_id)  # Fetch user from the database


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
                traceback.print_exc()
                return reg_error(e)  # handle errors here
        else:
            return reg_error()

        # Successfully registered
        # TODO: Link dashboard or something
        # TODO: Set flask session
        session["account_id"] = account.account_id
        return redirect(url_for("admin_myrestaurant"))

    return render_template("admin/register.html")


@app.route("/admin/logout")
def admin_logout():
    # TODO: Replace with flask-login
    if "account_id" in session:
        logging.info("admin_logout(): Admin %s logged out"
                     % gabi(session["account_id"]).get_email())
        del session["account_id"]
    else:
        logging.info("admin_logout(): Failed logout - lag or click twice")

    logout_user()
    return redirect(url_for("admin_home"))


# API for updating account, to be called by Account Settings
@app.route("/admin/updateAccount", methods=["GET", "POST"])
def admin_update_account():
    # TODO: Implement admin account soft-deletion
    #       and update restaurant name

    if request.method == "GET":
        flash("fail")
        return redirect(url_for("admin_home"))
    if not is_account_id_in_session():
        flash("fail")
        return redirect(url_for("admin_home"))

    # Check if current password entered was correct
    if not is_account_id_in_session() \
            .check_password_hash(request.form["updateSettingsPw"]):
        flash("Current Password is Wrong")
        return redirect(url_for("admin_home"))

    response = ""
    if "changeName" in request.form:
        if request.form["changeName"] != "":
            flash("Successfully updated account name from %s to %s"
                  % (getattr(is_account_id_in_session(), "name"),
                     request.form["changeName"]))
            is_account_id_in_session().restaurant_name = request.form["changeName"]

    if "changeEmail" in request.form:
        if request.form["changeEmail"] != "":
            result = (is_account_id_in_session()
                      .set_email(request.form["changeEmail"]))
            if result == Account.EMAIL_CHANGE_SUCCESS:
                flash("Successfully updated email")
            elif result == Account.EMAIL_CHANGE_ALREADY_EXISTS:
                flash("Failed updating email, Email already Exists")
            elif result == Account.EMAIL_CHANGE_INVALID:
                flash("Failed updating email, email is Invalid")

    if "changePw" in request.form:
        if request.form["changePw"] != request.form["changePwConfirm"]:
            flash("Confirm Password does not match Password")
        elif request.form["changePw"] != "":
            is_account_id_in_session() \
                .set_password_hash(request.form["changePw"])
            flash("Successfully updated password")

    save_account_db()
    return redirect(url_for("admin_home"))


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
    create_food_form = CreateFoodForm(request.form)

    # For the add food form
    MAX_SPECIFICATION_ID = 5  # for adding food
    MAX_TOPPING_ID = 8

    food_dict = {}
    with shelve.open("foodypulse", "c") as db:
        try:
            if 'food' in db:
                food_dict = db['food']
            else:
                db['food'] = food_dict
        except Exception as e:
            logging.error("create_food: error opening db (%s)" % e)

    # storing the food keys in food_dict into a new list for displaying and deleting
    food_list = []
    for key in food_dict:
        food = food_dict.get(key)
        food_list.append(food)

    return render_template('admin/foodManagement.html',
                           create_food_form=create_food_form,
                           MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                           MAX_TOPPING_ID=MAX_TOPPING_ID,
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
        food_dict = {}
        with shelve.open("foodypulse", "c") as db:
            try:
                if 'food' in db:
                    food_dict = db['food']
                else:
                    db['food'] = food_dict
            except Exception as e:
                logging.error("create_food: error opening db (%s)" % e)

            # Create a new food object
            food = Food(request.form["image"], create_food_form.item_name.data,
                        create_food_form.description.data,
                        create_food_form.price.data, create_food_form.allergy.data)

            food.specification = get_specs()  # set specifications as a List
            food.topping = get_top()  # set topping as a List
            food_dict[food.get_food_id()] = food  # set the food_id as key to store the food object
            db['food'] = food_dict

        # writeback
        with shelve.open("foodypulse", 'c') as db:
            db['food'] = food_dict

        return redirect(url_for('food_management'))

    return render_template('admin/addFoodForm.html', form=create_food_form,
                           MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                           MAX_TOPPING_ID=MAX_TOPPING_ID, )


@app.route('/deleteFood/<int:id>', methods=['POST'])
def delete_food(id):
    food_dict = {}
    with shelve.open("foodypulse", 'c') as db:
        food_dict = db['food']
        food_dict.pop(id)
        db['food'] = food_dict

    return redirect(url_for('food_management'))


@app.route('/updateFood/<int:id>/', methods=['GET', 'POST'])
# save new specification and list
def update_food(id):
    update_food_form = CreateFoodForm(request.form)
    if request.method == 'POST' and update_food_form.validate():
        food_dict = {}
        try:
            with shelve.open("foodypulse", 'w') as db:
                food_dict = db['food']
                food = food_dict.get(id)
                food.set_image(request.form["image"])
                food.set_name(update_food_form.item_name.data)
                food.set_description(update_food_form.description.data)
                food.set_price(update_food_form.price.data)
                food.set_allergy(update_food_form.allergy.data)
                db["food"] = food_dict
        except Exception as e:
            logging.error("update_customer: %s" % e)
            print("an error has occured in update customer")

        return redirect("/admin/foodManagement")
    else:
        food_dict = {}
        try:
            with shelve.open("foodypulse", 'r') as db:
                food_dict = db['food']

                food = food_dict.get(id)
                update_food_form.item_name.data = food.get_name()
                update_food_form.description.data = food.get_description()
                update_food_form.price.data = food.get_price()
                update_food_form.allergy.data = food.get_allergy()
        except:
            print("Error occured when update food")

        return render_template('admin/updateFood.html',
                               form=update_food_form,
                               MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                               MAX_TOPPING_ID=MAX_TOPPING_ID)


# @app.route('/updateFood/<int:id>/', methods=['GET', 'POST'])
#
# #save new specification and list
#
# def update_food(id):
#     update_food_form = CreateFoodForm(request.form)
#
#     # get specifications as a List, no WTForms
#     def get_specs() -> list:
#         specs = []
#
#         # do specifications exist in first place?
#         for i in range(MAX_SPECIFICATION_ID + 1):
#             if "specification%d" % i in request.form:
#                 specs.append(request.form["specification%d" % i])
#             else:
#                 break
#
#         logging.info("create_food: specs is %s" % specs)
#         return specs
#
#         # get toppings as a List, no WTForms
#
#     def get_top() -> list:
#         top = []
#
#         # do toppings exist in first place?
#         for i in range(MAX_TOPPING_ID + 1):
#             if "topping%d" % i in request.form:
#                 top.append(request.form["topping%d" % i])
#             else:
#                 break
#
#         logging.info("create_food: top is %s" % top)
#         return top
#
#
#     if request.method == 'POST' and update_food_form.validate():
#         food_dict = {}
#         with shelve.open("foodypulse", 'w') as db:
#             food_dict = db['food']
#
#             food = food_dict.get(id)
#             food.set_image(request.form["image"])
#             food.set_name(update_food_form.item_name.data)
#             food.set_description(update_food_form.description.data)
#             food.set_price(update_food_form.price.data)
#             food.set_allergy(update_food_form.allergy.data)
#             food.specification = get_specs()  # set specifications as a List
#             food.topping = get_top()  # set topping as a List
#
#             db['food'] = food_dict
#
#         return redirect(url_for('food_management'))
#     else:
#         food_dict = {}
#         with shelve.open("foodypulse", 'r') as db:
#             food_dict = db['food']
#
#         food = food_dict.get(id)
#         update_food_form.item_name.data = food.get_name()
#         update_food_form.description.data = food.get_description()
#         update_food_form.price.data = food.get_price()
#         update_food_form.allergy.data = food.get_allergy()
#         food.specification = get_specs()  # set specifications as a List
#         food.topping = get_top()  # set topping as a List
#
#         return render_template('admin/updateFood.html', form=update_food_form)

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


# @app.route('/updateFood/<int:id>/', methods=['GET', 'POST'])
# def update_food(id):
#     update_food_form = CreateFoodForm(request.form)
#     if request.method == 'POST' and update_food_form.validate():
#
#         with shelve.open(DB_NAME, 'c') as db:
#             food_dict = db['food']
#
#             user = food_dict.get(id)
#             user.set_image(request.form["image"])
#             user.set_name(update_food_form.item_name.data)
#             user.set_description(update_food_form.description.data)
#             user.set_price(update_food_form.price.data)
#             user.set_allergy(update_food_form.allergy.data)
#             user.set_topping(update_food_form.topping.data)
#
#             db['food'] = food_dict
#         db.close()
#
#         return redirect(url_for('retrieve_users'))
#     else:
#
#         db = shelve.open('user.db', 'r')
#         users_dict = db['Users']
#         db.close()
#
#         user = users_dict.get(id)
#         update_user_form.first_name.data = user.get_first_name()
#         update_user_form.last_name.data = user.get_last_name()
#         update_user_form.gender.data = user.get_gender()
#         update_user_form.membership.data = user.get_membership()
#         update_user_form.remarks.data = user.get_remarks()
#
#         return render_template('updateUser.html', form=update_user_form)
#


@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user_lls(id):
    food_list = []
    with shelve.open('foodypulse', 'c') as db:
        food_list = db['food']
        food_list.pop(id)
        db['food'] = food_list
    return "Deleted!!!!!!"


# <------------------------- YONGLIN ------------------------------>
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
# C (Create)
@app.route('/admin/create-restaurant', methods=['GET', 'POST'])
def admin_myrestaurant():  # ruri
    restaurant_details_form = RestaurantDetailsForm(request.form) # Using the Create Restaurant Form
    create_restaurant = Restaurant_controller() # Creating a controller / The controller will be the place where we do all the interaction
    if request.method == 'POST' and restaurant_details_form.validate():
        #  The Below code is using one of the controller's method "Create_restaurant"
        # It's passing in the form argument to instantiate the restaurant object
        restaurant_id = uuid.uuid4().hex
        create_restaurant.create_restaurant(
            restaurant_id,
            restaurant_details_form.rest_name.data,
            request.form["rest_logo"],
            restaurant_details_form.rest_contact.data,
            restaurant_details_form.rest_hour_open.data,
            restaurant_details_form.rest_hour_close.data,
            restaurant_details_form.rest_address1.data,
            restaurant_details_form.rest_address2.data,
            restaurant_details_form.rest_postcode.data,
            restaurant_details_form.rest_desc.data,
            restaurant_details_form.rest_bank.data,
            restaurant_details_form.rest_del1.data,
            restaurant_details_form.rest_del2.data,
            restaurant_details_form.rest_del3.data,
            restaurant_details_form.rest_del4.data,
            restaurant_details_form.rest_del5.data
        )
        # flask_login.current_user.restaurant = restaurant_id
        # Once done, it'll redirect to the home page
        return redirect(url_for('admin_home'))
    restaurants_dict = {}
    # if request.method == 'POST' and restaurant_details_form.validate():
    #     db = shelve.open(DB_NAME, 'c')
    #     try:
    #         restaurants_dict = db['Restaurants']
    #     except Exception as e:
    #         logging.error("Error in retriedb file doesn't existving Restaurants from "
    #                       "restaurants.db (%s)" % e)

        # user_id = session["account_id"]
        # user_object = Restaurant_controller()
        # get_user_object = user_object.find_user_by_id(user_id)

        # restaurant = Restaurant(uuid.uuid4().hex,
        #                         # request.form["alltasks"],
        #                         restaurant_details_form.rest_name.data,
        #                         request.form["rest_logo"],
        #                         restaurant_details_form.rest_contact.data,
        #                         restaurant_details_form.rest_hour_open.data,
        #                         restaurant_details_form.rest_hour_close.data,
        #                         restaurant_details_form.rest_address1.data,
        #                         restaurant_details_form.rest_address2.data,
        #                         restaurant_details_form.rest_postcode.data,
        #                         restaurant_details_form.rest_desc.data,
        #                         restaurant_details_form.rest_bank.data,
        #                         restaurant_details_form.rest_del1.data,
        #                         restaurant_details_form.rest_del2.data,
        #                         restaurant_details_form.rest_del3.data,
        #                         restaurant_details_form.rest_del4.data,
        #                         restaurant_details_form.rest_del5.data)
        #
        # # print(uuid.uuid4().hex())
        # restaurants_dict[restaurant.get_id()] = restaurant
        # db['Restaurants'] = restaurants_dict
        # db.close()
        # return redirect(url_for('admin_home'))

    return render_template("admin/restaurant.html", form=restaurant_details_form,  restaurant=all_restaurant())


# R (Read)
# This is the route that displays all the relevant restaurant details
@app.route('/admin/my-restaurantV2')
def view_restaurant():
    return render_template('admin/myrestaurantv2.html',restaurant=all_restaurant())



# U (Update Form) # This route is to showcase the update route
# This route contains the form that allows us to update the restaurant details
@app.route('/updateRestaurant/<id>', methods=['GET', 'POST'])
def update_restaurant(id):
    edit_restaurant = RestaurantDetailsForm(request.form)
    restaurant = filter(lambda r : r.get_id() == id, all_restaurant()) # Array Filtering that allows me to track which restaurant the restaurant belongs to for example (ID 1 == ID 1)
    # This lambda is a callback function, it's pretty much comparing if the ID of the restaurant is equal to our id argument
    if request.method == 'POST' and edit_restaurant.validate():
        return render_template('updateuserv2.html', form=edit_restaurant, restaurant=restaurant)
    return render_template('updateuserv2.html', form=edit_restaurant, restaurant=all_restaurant())




# U (Update)
@app.route('/updateRestaurantConfirm/<id>', methods=['GET', 'POST'])
def update_restaurant_confirm(id):
    edit_restaurant = EditRestaurantDetailsForm(request.form)
    editing_restaurant = Restaurant_controller()
    if request.method == 'POST' and edit_restaurant.validate():
        editing_restaurant.edit_restaurant(
            id,
            edit_restaurant.rest_name.data,
            request.form["rest_logo"],
            edit_restaurant.rest_contact.data,
            edit_restaurant.rest_hour_open.data,
            edit_restaurant.rest_hour_close.data,
            edit_restaurant.rest_address1.data,
            edit_restaurant.rest_address2.data,
            edit_restaurant.rest_postcode.data,
            edit_restaurant.rest_desc.data,
            edit_restaurant.rest_bank.data,
            edit_restaurant.rest_del1.data,
            edit_restaurant.rest_del2.data,
            edit_restaurant.rest_del3.data,
            edit_restaurant.rest_del4.data,
            edit_restaurant.rest_del5.data
        )
    return redirect(url_for('view_restaurant'))




@app.route('/admin/my-restaurant')
def retrieve_restaurant():
    restaurants_dict = {}
    db = shelve.open(DB_NAME, 'r')
    restaurants_dict = db['Restaurants']
    db.close()
    restaurants_list = []
    for key in restaurants_dict:
        restaurant = restaurants_dict.get(key)
        restaurants_list.append(restaurant)

    return render_template('admin/myrestaurant.html', count=len(restaurants_list), restaurants_list=restaurants_list)

# @app.route('/updateRestaurant/<int:id>/', methods=['GET', 'POST'])
# def update_restaurant(id):
#     update_restaurant_form = RestaurantDetailsForm(request.form)
#     if request.method == 'POST' and update_restaurant_form.validate():
#         users_dict = {}
#         db = shelve.open('restaurant.db', 'w')
#         restaurants_dict = db['Users']
#
#         user = users_dict.get(id)
#         user.set_first_name(update_restaurant_form.first_name.data)
#         user.set_last_name(update_restaurant_form.last_name.data)
#         user.set_gender(update_restaurant_form.gender.data)
#         user.set_membership(update_restaurant_form.membership.data)
#         user.set_remarks(update_restaurant_form.remarks.data)
#
#         db['Restaurants'] = restaurants_dict
#         db.close()
#
#         return redirect(url_for('retrieve_users'))
#     else:
#         users_dict = {}
#         db = shelve.open('user.db', 'r')
#         users_dict = db['Users']
#         db.close()
#
#         user = users_dict.get(id)
#         update_user_form.first_name.data = user.get_first_name()
#         update_user_form.last_name.data = user.get_last_name()
#         update_user_form.gender.data = user.get_gender()
#         update_user_form.membership.data = user.get_membership()
#         update_user_form.remarks.data = user.get_remarks()
#
#         return render_template('updateUser.html', form=update_user_form)

# Temporarily removed code here due to breaking the program-ashlee
