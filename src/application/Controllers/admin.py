# Controller for the Admin side of things.
# Do NOT run directly. Run main.py in the appdpj/src/ directory instead.

# New routes go here, not in __init__.
import datetime
import traceback

import flask
from flask import render_template, request, redirect, url_for, session, flash, Flask
from flask_login import logout_user, login_required, current_user, login_user

from application.CouponForms import CreateCouponForm
from application.Models.Admin import *
from application.Models.CouponSystem import CouponSystem
from application.Models.Certification import Certification
from application.Models.Food import Food
from application.Models.Restaurant import Restaurant
from application import app, login_manager
from application.Models.Transaction import Transaction
from application.adminAddFoodForm import CreateFoodForm
from werkzeug.utils import secure_filename
from application.Controllers.restaurant_controller import *
# from application.restaurantCertification import DocumentUploadForm
import shelve, os
import uuid
from application.rest_details_form import *

# Ruri's imported libraries
import urllib.request
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf'])


# <------------------------- ASHLEE ------------------------------>

@app.route("/admin")
# @app.route("/admin/home")
@login_required
def admin_home():  # ashlee
    return render_template("admin/home.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():  # ashlee
    # TODO: Refactor with flask-login
    # if already logged in, what's the point?
    # if is_account_id_in_session():
    #     return redirect(url_for("admin_home"))

    def login_error():
        return redirect("%s?error=1" % url_for("admin_login"))

    if request.method == "POST":
        # That means user submitted login form. Check errors.
        login = Account.check_credentials(request.form["email"],
                                          request.form["password"])
        if login is not None:
            with shelve.open(ACCOUNT_DB, 'c') as db:
                accounts = db["accounts"]
                accounts[login.account_id].authenticated = True
                db["accounts"] = accounts

            login_user(login)
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
                and request.form["password"] == request.form["passwordAgain"]
                and 4 <= len(request.form["password"]) <= 20):
            try:
                account = Admin(request.form["name"], request.form["email"],
                                request.form["password"])
            except Exception as e:
                logging.info("admin_register: error %s" % e)
                traceback.print_exc()
                return reg_error(e)  # handle errors here
        else:
            return reg_error()

        # Successfully authenticated
        with shelve.open("accounts", 'c') as db:
            accounts = db["acocunts"]
            # For Flask-login
            accounts[account.account_id].authenticated = True
            login_user(account)

            # TEMPORARY FOR WEEK 13
            coupon_systems_list = []

            with shelve.open("coupon", 'c') as db:
                if "coupon_systems" in db:
                    coupon_systems_list = db["coupon_systems"]
                else:
                    coupon_systems_list.append(CouponSystem())

        coupon_systems_list.append(CouponSystem())
        # TODO: Refactor coupons

        with shelve.open("coupon", 'c') as db:
            db["coupon_systems"] = coupon_systems_list

        return redirect(url_for("admin_myrestaurant"))

    return render_template("admin/register.html")


@app.route("/admin/logout")
@login_required
def admin_logout():
    # TODO: Replace with flask-login
    # Logout the current user
    current_user.authenticated = False
    with shelve.open("accounts", 'c') as db:
        accounts = db["accounts"]
        accounts[current_user.account_id] = current_user

    logout_user()
    return redirect(url_for("admin_home"))


# API for updating account, to be called by Account Settings
@app.route("/admin/updateAccount", methods=["GET", "POST"])
@login_required
def admin_update_account():
    # TODO: Implement admin account soft-deletion
    #       and update restaurant name

    if request.method == "GET":
        flash("fail")
        return redirect(url_for("admin_home"))

    # Check if current password entered was correct
    if not current_user.check_password_hash(request.form["updateSettingsPw"]):
        flash("Current Password is Wrong")
        return redirect(url_for("admin_home"))

    with shelve.open("accounts", 'c') as db:
        accounts = db["accounts"]

        response = ""
        if "changeName" in request.form:
            if request.form["changeName"] != "":
                current_user.restaurant_name = request.form["changeName"]

        if "changeEmail" in request.form:
            if request.form["changeEmail"] != "":
                result = (current_user.set_email(request.form["changeEmail"]))
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
                current_user.set_password_hash(request.form["changePw"])
                flash("Successfully updated password")

        accounts[current_user.account_id] = current_user  # save back
    return redirect(url_for("admin_home"))


@app.route("/admin/deleteAccount")
def delete_admin_account():
    if current_user:
        current_user.hard_delete_account()
        flash("Successfully deleted your account")
    else:
        flash("Failed to delete your account!")

    return redirect(url_for("admin_logout"))


# for testing only - to remove on final!
@app.route("/admin/coupon/createExamples")
@login_required
def admin_coupon_add_examples():
    coupon_systems_list = []

    with shelve.open("coupon", 'c') as db:
        if "coupon_systems" in db:
            coupon_systems_list = db["coupon_systems"]
        else:
            coupon_systems_list.append(CouponSystem())

    # TEMPORARY FOR WEEK 13 ONLY
    # session["coupon_systems_active_idx"] = 0
    active_coupon_system_idx = session["coupon_systems_active_idx"]

    coupon_systems_list[active_coupon_system_idx].new_coupon("FoodyPulse3",
                                                             ["All: Spaghetti"],
                                                             CouponSystem.Discount.PERCENTAGE_OFF,
                                                             10,
                                                             (datetime.datetime.datetime(2022, 3, 1)))

    coupon_systems_list[active_coupon_system_idx].new_coupon("Meowbie9",
                                                             ["All: Drinks"],
                                                             CouponSystem.Discount.PERCENTAGE_OFF,
                                                             20,
                                                             (datetime.datetime.datetime(2022, 1, 21)))

    coupon_systems_list[active_coupon_system_idx].new_coupon("CnySpecial",
                                                             ["All: Drinks"],
                                                             CouponSystem.Discount.FIXED_PRICE,
                                                             3.5,
                                                             (datetime.datetime.datetime(2022, 2, 14)))

    with shelve.open("coupon", 'c') as db:
        db["coupon_systems"] = coupon_systems_list

    return redirect(url_for("admin_coupon_management"))


@app.route("/admin/coupon")
@login_required
def admin_coupon_management():
    # TODO: Replace with flask-login
    # if not logged in, need to login first
    # if not is_account_id_in_session():
    #     return redirect(url_for("admin_login"))

    coupon_systems_list = []

    with shelve.open("coupon", 'c') as db:
        if "coupon_systems" in db:
            coupon_systems_list = db["coupon_systems"]
        else:
            coupon_systems_list.append(CouponSystem())

    # TEMPORARY FOR WEEK 13 ONLY
    # session["coupon_systems_active_idx"] = 0
    active_coupon_system_idx = session["coupon_systems_active_idx"]
    selected_system = coupon_systems_list[active_coupon_system_idx]

    with shelve.open("coupon", 'c') as db:
        db["coupon_systems"] = coupon_systems_list

    return render_template("admin/retrieveCoupons.html",
                           len=len,
                           coupon_list=selected_system.list_of_coupons)


@app.route("/admin/addCoupon", methods=["GET", "POST"])
def admin_coupon_add():  # todo
    # TODO: Replace with flask-login
    # if not logged in, need to login first
    if not is_account_id_in_session():
        return redirect(url_for("admin_login"))

    create_coupon_form = CreateCouponForm()
    if request.method == "POST" and create_coupon_form.validate():
        coupon_systems_list = []

        with shelve.open("coupon", 'c') as db:
            if "coupon_systems" in db:
                coupon_systems_list = db["coupon_systems"]
            else:
                coupon_systems_list.append(CouponSystem())

        active_coupon_system_idx = session["coupon_systems_active_idx"]
        cs = coupon_systems_list[active_coupon_system_idx]

        discount_type = (CouponSystem.Discount.FIXED_PRICE if
                         create_coupon_form.discount_type.data == "fp" else
                         CouponSystem.Discount.PERCENTAGE_OFF)

        cs.new_coupon(create_coupon_form.coupon_code.data,
                      create_coupon_form.food_items.data,
                      discount_type,
                      create_coupon_form.discount_amount.data,
                      create_coupon_form.expiry.data)

        with shelve.open("coupon", 'c') as db:
            db["coupon_systems"] = coupon_systems_list

        return redirect(url_for("admin_coupon_management"))
    else:
        return render_template("admin/createCoupon.html", form=create_coupon_form)


@app.route("/admin/updateCoupon/<int:idx>")  # index of in coupon systems
def admin_coupon_update(idx):  # todo: handle active systems
    # TODO: Replace with flask-login
    # if not logged in, need to login first
    if not is_account_id_in_session():
        return redirect(url_for("admin_login"))

    flash("Under Construction")
    return redirect(url_for("admin_coupon_management"))


@app.route("/admin/deleteCoupon/<int:id>", methods=["GET", "POST"])
def admin_coupon_delete(id):  # todo: handle active systems
    # TODO: Replace with flask-login
    # if not logged in, need to login first
    if not is_account_id_in_session():
        return redirect(url_for("admin_login"))

    coupon_systems_list = []

    with shelve.open("coupon", 'c') as db:
        if "coupon_systems" in db:
            coupon_systems_list = db["coupon_systems"]
        else:
            coupon_systems_list.append(CouponSystem())

    active_coupon_system_idx = session["coupon_systems_active_idx"]
    cs = coupon_systems_list[active_coupon_system_idx]

    for coupon in cs.list_of_coupons:
        if coupon.id == id:
            cs.list_of_coupons.remove(coupon)

    with shelve.open("coupon", 'c') as db:
        db["coupon_systems"] = coupon_systems_list

    return redirect(url_for("admin_coupon_management"))


# <------------------------- CLARA ------------------------------>
# APP ROUTE TO FOOD MANAGEMENT clara
@app.route("/admin/foodManagement")
def food_management():
    create_food_form = CreateFoodForm(request.form)

    # For the add food form
    MAX_SPECIFICATION_ID = 2  # for adding food
    MAX_TOPPING_ID = 3

    food_dict = {}
    with shelve.open("foodypulse", "c") as db:
        try:
            if 'food' in db:
                food_dict = db['food']
            else:
                db['food'] = food_dict
        except Exception as e:
            logging.error("create_food: error opening db (%s)" % e)

    # storing the food keys in food_dict into a new list for displaying and
    # deleting
    food_list = []
    for key in food_dict:
        food = food_dict.get(key)
        food_list.append(food)

    return render_template('admin/foodManagement.html',
                           create_food_form=create_food_form,
                           MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                           MAX_TOPPING_ID=MAX_TOPPING_ID,
                           food_list=food_list)


MAX_SPECIFICATION_ID = 2  # for adding food
MAX_TOPPING_ID = 3


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
                        create_food_form.price.data,
                        create_food_form.allergy.data)

            food.specification = get_specs()  # set specifications as a List
            food.topping = get_top()  # set topping as a List
            food_dict[food.get_food_id()] = food  # set the food_id as key to store
            # the food object
            db['food'] = food_dict

        # writeback
        with shelve.open("foodypulse", 'c') as db:
            db['food'] = food_dict

        return redirect(url_for('food_management'))

    return render_template('admin/addFoodForm.html', form=create_food_form,
                           MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                           MAX_TOPPING_ID=MAX_TOPPING_ID, )


# Note from Ashlee: when doing integration, please prefix all URLs with /admin/
@app.route('/deleteFood/<int:id>', methods=['POST'])
def delete_food(id):
    food_dict = {}
    with shelve.open("foodypulse", 'c') as db:
        food_dict = db['food']
        food_dict.pop(id)
        db['food'] = food_dict

    return redirect(url_for('food_management'))


# Note from Ashlee: when doing integration, please prefix all URLs with /admin/
# save new specification and list
@app.route('/updateFood/<int:id>/', methods=['GET', 'POST'])
def update_food(id):
    update_food_form = CreateFoodForm(request.form)

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

    if request.method == 'POST' and update_food_form.validate():
        food_dict = {}
        try:
            with shelve.open("foodypulse", 'w') as db:
                food_dict = db['food']
                food = food_dict.get(id)
                # food.set_image = request.form["image"]
                food.set_name(update_food_form.item_name.data)
                food.set_description(update_food_form.description.data)
                food.set_price(update_food_form.price.data)
                food.set_allergy(update_food_form.allergy.data)
                food.specification = get_specs()  # set specifications as a List
                food.topping = get_top()  # set topping as a List
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

                # food.get_image(request.form["image"])
                update_food_form.item_name.data = food.get_name()
                update_food_form.description.data = food.get_description()
                update_food_form.price.data = food.get_price()
                update_food_form.allergy.data = food.get_allergy()

                # for food in food_dict:
                #     food.get_specification()
                #     food.get_topping()
                #
        except:
            print("Error occured when update food")

        return render_template('admin/updateFood.html',
                               form=update_food_form,
                               food=food,
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
# YL: for transactions -- creating of dummy data
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

    t2 = Transaction()  # t2
    t2.account_name = 'Ching Chong'
    t2.set_option('Dine-in')
    t2.set_price(80.90)
    t2.set_used_coupons('50PASTA')
    t2.set_ratings(5)
    transaction_list.append(t2)

    t3 = Transaction()  # t3
    t3.account_name = 'Hosea'
    t3.set_option('Delivery')
    t3.set_price(20.10)
    t3.set_used_coupons('50PASTA')
    t3.set_ratings(1)
    transaction_list.append(t3)

    t4 = Transaction()  # t4
    t4.account_name = 'Clara'
    t4.set_option('Delivery')
    t4.set_price(58.30)
    t4.set_used_coupons('SPAGETIT')
    t4.set_ratings(2)
    transaction_list.append(t4)

    t5 = Transaction()  # t5
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

    t8 = Transaction()
    t8.account_name = 'Lolita'
    t8.set_option('Delivery')
    t8.set_price(50.30)
    t8.set_used_coupons('SPAGETIT')
    t8.set_ratings(2)
    transaction_list.append(t8)

    t9 = Transaction()  # t2
    t9.account_name = 'Cheryln'
    t9.set_option('Dine-in')
    t9.set_price(80.90)
    t9.set_used_coupons('50PASTA')
    t9.set_ratings(5)
    transaction_list.append(t9)

    t10 = Transaction()  # t4
    t10.account_name = 'Swee Koon'
    t10.set_option('Delivery')
    t10.set_price(58.30)
    t10.set_used_coupons('SPAGETIT')
    t10.set_ratings(2)
    transaction_list.append(t10)

    t11 = Transaction()  # t5
    t11.account_name = 'Adrian'
    t11.set_option('Dine-in')
    t11.set_price(80.90)
    t11.set_used_coupons('50PASTA')
    t11.set_ratings(3)
    transaction_list.append(t11)

    t12 = Transaction()  # t6
    t12.account_name = 'Ryan'
    t12.set_option('Delivery')
    t12.set_price(100.10)
    t12.set_used_coupons('50PASTA')
    t12.set_ratings(2)
    transaction_list.append(t12)

    t13 = Transaction()
    t13.account_name = 'Sammi'
    t13.set_option('Dine-in')
    t13.set_price(10.90)
    t13.set_used_coupons('50PASTA')
    t13.set_ratings(4)
    transaction_list.append(t13)

    t14 = Transaction()  # t4
    t14.account_name = 'Vianna'
    t14.set_option('Delivery')
    t14.set_price(58.30)
    t14.set_used_coupons('SPAGETIT')
    t14.set_ratings(2)
    transaction_list.append(t14)

    t15 = Transaction()  # t5
    t15.account_name = 'Dylan'
    t15.set_option('Dine-in')
    t15.set_price(80.90)
    t15.set_used_coupons('50PASTA')
    t15.set_ratings(3)
    transaction_list.append(t15)

    t16 = Transaction()  # t6
    t16.account_name = 'Chit Boon'
    t16.set_option('Delivery')
    t16.set_price(100.10)
    t16.set_used_coupons('50PASTA')
    t16.set_ratings(2)
    transaction_list.append(t16)

    t17 = Transaction()
    t17.account_name = 'Kit Fan'
    t17.set_option('Dine-in')
    t17.set_price(10.90)
    t17.set_used_coupons('50PASTA')
    t17.set_ratings(4)
    transaction_list.append(t17)

    t18 = Transaction()
    t18.account_name = 'Gabriel Choo'
    t18.set_option('Delivery')
    t18.set_price(50.30)
    t18.set_used_coupons('SPAGETIT')
    t18.set_ratings(2)
    transaction_list.append(t18)

    t19 = Transaction()  # t2
    t19.account_name = 'Bryan Hoo'
    t19.set_option('Dine-in')
    t19.set_price(80.90)
    t19.set_used_coupons('50PASTA')
    t19.set_ratings(5)
    transaction_list.append(t19)

    t20 = Transaction()  # t3
    t20.account_name = 'Yuen Loong'
    t20.set_option('Delivery')
    t20.set_price(20.10)
    t20.set_used_coupons('50PASTA')
    t20.set_ratings(1)
    transaction_list.append(t20)

    # writing to the database
    with shelve.open(DB_NAME, "c") as db:
        try:
            db['shop_transactions'] = transaction_list
        except Exception as e:
            logging.error("create_example_transactions: error writing to db (%s)" % e)

    return redirect(url_for("admin_transaction"))


# YL: for transactions -- reading of data and displaying (R in CRUD)
@app.route("/admin/transaction")
def admin_transaction():
    # read transactions from db
    with shelve.open(DB_NAME, 'c') as db:
        if 'shop_transactions' in db:
            transaction_list = db['shop_transactions']
            print(db['shop_transactions'])
            logging.info("admin_transaction: reading from db['shop_transactions']"
                         ", %d elems" % len(db["shop_transactions"]))
        else:
            logging.info("admin_transaction: nothing found in db, starting empty")
            transaction_list = []

    def get_transaction_by_id(transaction_id):  # debug
        for transaction in transaction_list:
            if transaction_id == transaction.count_id:
                return transaction

    return render_template("admin/transaction.html",
                           count=len(transaction_list),
                           transaction_list=transaction_list)


# YL: for transactions -- soft delete (D in CRUD)
# soft delete -> restaurant can soft delete transactions jic if the transaction is cancelled
@app.route('/admin/transaction/delete/<transaction_id>')
def delete_transaction(transaction_id):
    transaction_id = int(transaction_id)

    transaction_list = []
    with shelve.open(DB_NAME, 'c') as db:
        for transaction in db['shop_transactions']:
            transaction_list.append(transaction)

    def get_transaction_by_id(t_id):  # debug
        for t in transaction_list:
            if t_id == t.count_id:
                return t

    logging.info("delete_transaction: deleted transaction with id %d"
                 % transaction_id)

    # set instance attribute 'deleted' of Transaction.py = False
    get_transaction_by_id(transaction_id).deleted = True

    # writeback to shelve
    with shelve.open(DB_NAME, 'c') as db:
        db["shop_transactions"] = transaction_list

    return redirect(url_for('admin_transaction'))


# certification -- xu yong lin
# YL: for certification -- form (C in CRUD)
@app.route("/admin/uploadCertification")
def test_upload():
    return render_template("admin/certification.html")


# def upload_cert():
#     certification_dict = {}
#     nb = 'NIL'
#     npnl = 'NIL'
#     if request.method == 'POST':
#
#         with shelve.open(DB_NAME, 'c') as db:
#             try:
#                 certification_dict = db['certification']
#                 print(certification_dict)
#             except Exception as e:
#                 logging.error("Error in retrieving certificate from ""certification.db (%s)" % e)
#             # create a new Certification Object
#             certchecks = request.form.getlist('certCheck')
#             print(certchecks)
#             for i in certchecks:
#                 if 'NoBeef' in certchecks:
#                     nb = 'YES'
#                 elif 'NoPorkNoLard' in certchecks:
#                     npnl = 'Yes'
#                 else:
#                     print('something is wrong ')
#             print(npnl)
#             print(nb)
#
#             certification = Certification(request.form["hygieneDocument"], request.form["halalDocument"],
#                                           request.form["vegetarianDocument"], request.form["veganDocument"],
#                                           npnl, nb)
#             certification_dict[certification.id] = certification
#             db['certification'] = certification_dict
#
#             return redirect(url_for('read_cert'))
#         # update: cert dict => get the correct cert by id
#
#     return render_template("admin/certification.html")


# YL: for certification -- reading of data and displaying it to myRestaurant (C in CRUD)

@app.route('/admin/uploader', methods=['GET', 'POST'])
def uploader():
    certification_dict = {}
    nb = 'NIL'
    npnl = 'NIL'
    if request.method == 'POST':
        app.config['UPLOADED_PDF'] = 'application/static/restaurantCertification/'

        with shelve.open(DB_NAME, 'c') as db:
            try:
                certification_dict = db['certification']
                print(certification_dict)
            except Exception as e:
                logging.error("uploader: ""certification.db (%s)" % e)

            # create a new certification object
            # certchecks = request.form.getlist('certCheck')
            # print(certchecks)
            # for i in certchecks:
            #     if 'NoBeef' in certchecks:
            #         nb = 'YES'
            #     elif 'NoPorkNoLard' in certchecks:
            #         npnl = 'Yes'
            #     else:
            #         print('something is wrong ')
            # print(npnl)
            # print(nb)
            f = request.files['hygieneDocument']
            filename = secure_filename(f.filename)

            import os
            import os.path
            os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_PDF'])), exist_ok=True)
            f.save(os.path.join(os.getcwd(), app.config['UPLOADED_PDF']) + filename)

            logging.info('file uploaded successfully')
            cert = Certification(f)

            certification_dict['cert.id'] = cert
            db['certification'] = certification_dict

            return redirect(url_for('read_cert'))


@app.route("/admin/certification")
def read_cert():
    certification_dict = {}
    with shelve.open(DB_NAME, "c") as db:
        try:
            if 'certification' in db:
                certification_dict = db['certification']

            else:
                db['certification'] = certification_dict
                print(certification_dict)
                logging.info("read_cert: nothing found in db, starting empty")
        except Exception as e:
            logging.error("read_cert: error opening db (%s)" % e)

        certificate_list = []
        for key in certification_dict:
            food = certification_dict.get(key)
            certificate_list.append(food)

    return render_template("admin/certification2.html", certificate_list=certificate_list)


# YL: for certification -- Update certification [if it expires/needs to be updated] (U in CRUD)
# TODO: REDIRECT BACK TO FORM IN 'C IN CRUD'
# TODO: CHECK IF THE FILES ARE THE SAME AND UPDATE THE DETAILS
@app.route('/admin/updateCertification/<int:id>', methods=['GET', 'POST'])
def update_cert(id):
    nb = 'NIL'
    npnl = 'NIL'

    if request.method == 'POST':
        certification_dict = {}
        try:
            with shelve.open(DB_NAME, "c") as db:
                certification_dict = db['certification']

                # updating the information
                certchecks = request.form.getlist('certCheck')
                for i in certchecks:
                    if 'NoBeef' in certchecks:
                        nb = 'YES'
                    elif 'No Pork No Lard' in certchecks:
                        npnl = 'YES'
                    else:
                        print('something is wrong ')

                certification = certification_dict.get(id)
                # inset values of the updated thing inside
                certification.hygiene_cert = request.form["hygieneDocument"]
                certification.halal_cert = request.form["halalDocument"]
                certification.vegetarian_cert = request.form["vegetarianDocument"]
                certification.vegan_cert = request.form["veganDocument"]
                certification.noPorknoLard = npnl
                certification.noBeef = nb
                print(certification)

                # writeback
                db['certification'] = certification_dict
        except Exception as e:
            logging.error("Error in retrieving certificate from ""certification.db (%s)" % e)

        return redirect(url_for('read_cert'))
    else:
        certification_dict = {}
        id_list = []
        print('I am reading from shelve')
        try:
            # reading to display the pre-existing inputs
            with shelve.open(DB_NAME, "c") as db:
                certification_dict = db['certification']
        except Exception as e:
            logging.error("Error in retrieving certificate from ""certification.db (%s)" % e)

        c = certification_dict.get(id)
        id_list.append(c)
        print(c.hygiene_cert)
        return render_template('admin/updateCertification.html', id_list=id_list)


# YL: for certification -- Delete (D in CRUD)
# TODO: DELETE BUTTON (similar to delete User in SimpleWebApplication)
# not soft delete!
@app.route('/deleteCertification/<int:id>', methods=['POST'])
def delete_cert(id):
    with shelve.open(DB_NAME, 'w') as db:
        try:
            certification_dict = db['certification']
            if id in certification_dict:
                certification_dict.pop(id)
            db['certification'] = certification_dict
        except Exception as e:
            logging.error("delete_food: error opening db (%s)" % e)

    return redirect(url_for('read_cert'))


# def upload_cert():
#     i = 1
#     certification_form = DocumentUploadForm(request.form)
#     certifications_dict = {}
#     if request.method == 'POST' and certification_form.validate():
#         db = shelve.open(DB_NAME, 'c')
#         try:
#             certifications_dict = db['certification']
#         except Exception as e:
#             logging.error("Error in retrieving Certification from "
#                           "certification.db (%s)" % e)
#
#         certifications_dict[i] = i
#         db['certification'] = certifications_dict
#
#         db.close()
#
#     certification = Certification(request.form["hygieneDocument"])
#
#     # if certification_form.validate_on_submit():
#     #     # file path to save files to:
#     #     assets_dir = os.path.join(os.path.dirname(app.instance_path), 'restaurantCertification')
#     #     # assests_dir ==> C:\Users\yongl\appdpj\src\restaurantCertification
#     #     hygiene = certification_form.hygiene_doc.data
#     #
#     #     # saving
#     #     hygiene.save(os.path.join(assets_dir, 'hygiene', hygiene.filename))
#     #
#     #     logging.info('Document uploaded successfully.')
#     #     return redirect(url_for('admin_home'))
#
#     return render_template("admin/certification2.html")


# @app.route("/admin/certification", methods=['GET', 'POST'])
# def admin_certification():
#     # TODO: FILE UPLOAD, FILE SAVING, SHELVE UPDATE
#     # set upload directory path
#     certification_form = RestaurantCertification()
#     if certification_form.validate_on_submit():
#         assets_dir = os.path.join(os.path.dirname('./static/restaurantCertification'))
#
#         hygiene = certification_form.hygiene_cert.data
#         halal = certification_form.halal_cert.data
#         vegetarian = certification_form.vegetarian_cert.data
#         vegan = certification_form.vegan_cert.data
#
#         # document save
#         # halal.save(os.path.join(app.config['UPLOAD_FOLDER'], halaldoc_name))
#         hygiene.save(os.path.join(assets_dir, '<userid>', hygiene))
#         halal.save(os.path.join(assets_dir, '<userid>', halal))
#         vegetarian.save(os.path.join(assets_dir, '<userid>', vegetarian))
#         vegan.save(os.path.join(assets_dir, '<userid>', vegan))
#
#         # halal.save(os.path.join('/application/static/restaurantCertification', halaldoc_name))
#         # vegetarian.save(
#         #     os.path.join('/application/static/restaurantCertification', vegetariandoc_name))
#         # vegan.save(os.path.join('/application/static/restaurantCertification', vegandoc_name))
#
#         flash('Document uploaded successfully')
#
#         return redirect(url_for('admin_transaction'))
#
#     return render_template("admin/certification.html",
#                            certification_form=certification_form)


# <------------------------- RURI ------------------------------>
# C (Create)
@app.route('/admin/create-restaurant', methods=['GET', 'POST'])
def admin_myrestaurant():  # ruri
    restaurant_details_form = RestaurantDetailsForm(
        request.form)  # Using the Create Restaurant Form
    create_restaurant = Restaurant_controller()  # Creating a controller /
    # The controller will be the place where we do all the interaction
    if request.method == 'POST' and restaurant_details_form.validate():
        #  The Below code is using one of the controller's method
        #  "Create_restaurant"
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
    #         logging.error("Error in retriedb file doesn't existving
    #         Restaurants from "
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

    return render_template("admin/restaurant.html",
                           form=restaurant_details_form,
                           restaurant=all_restaurant())


# R (Read)
# This is the route that displays all the relevant restaurant details
@app.route('/admin/my-restaurantV2')
def view_restaurant():
    return render_template('admin/myrestaurantv2.html',
                           restaurant=all_restaurant())


# U (Update Form) # This route is to showcase the update route
# This route contains the form that allows us to update the restaurant details
@app.route('/updateRestaurant/<id>', methods=['GET', 'POST'])
def update_restaurant(id):
    edit_restaurant = RestaurantDetailsForm(request.form)
    restaurant = filter(lambda r: r.get_id() == id,
                        all_restaurant())  # Array Filtering that allows me
    # to track which restaurant the restaurant belongs to for example (ID 1
    # == ID 1)
    # This lambda is a callback function, it's pretty much comparing if the
    # ID of the restaurant is equal to our id argument
    if request.method == 'POST' and edit_restaurant.validate():
        return render_template('updateuserv2.html', form=edit_restaurant,
                               restaurant=restaurant)
    return render_template('updateuserv2.html', form=edit_restaurant,
                           restaurant=all_restaurant())


# U (Update)
@app.route('/updateRestaurantConfirm/<id>', methods=['GET', 'POST'])
def update_restaurant_confirm(id):
    edit_restaurant = RestaurantDetailsForm(request.form)
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

    return render_template('admin/myrestaurant.html',
                           count=len(restaurants_list),
                           restaurants_list=restaurants_list)


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

@app.route("/admin/dashboard")
def dashboard():  # ruri
    return render_template("admin/dashboard.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[
        1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run()
