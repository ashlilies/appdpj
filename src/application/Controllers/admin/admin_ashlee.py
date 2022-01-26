import functools
import os
import traceback
import uuid
from datetime import date

from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user, login_user
from werkzeug.utils import secure_filename

from application import app
from application.CouponForms import CreateCouponForm
from application.Models.Admin import *
from application.Models.CouponSystem import CouponSystem, FoodIdNotExistsError
from application.Models.Food2 import FoodDao
from application.CreateFoodForm import CreateFoodForm


# <------------------------- ASHLEE ------------------------------>

# Decorator to only allow admin accounts or guests

def admin_side(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if isinstance(current_user, Admin) or not current_user.is_authenticated:
            print(current_user)
            return view(*args, **kwargs)
        flash("You need to log out first to access the Admin side.")
        return redirect('/')

    return wrapper


@app.route("/admin")
@app.route("/admin/home", alias=True)
@admin_side
def admin_home():  # ashlee
    return render_template("admin/home.html")


@app.route("/admin/login", methods=["GET", "POST"])
@admin_side
def admin_login():  # ashlee
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
@admin_side
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
            accounts = db["accounts"]
            # For Flask-login
            accounts[account.account_id].authenticated = True
            db["accounts"] = accounts
            login_user(account)

        return redirect(url_for("admin_myrestaurant"))

    return render_template("admin/register.html")


@app.route("/admin/logout")
@login_required
@admin_side
def admin_logout():
    # Logout the current user
    current_user.authenticated = False
    with shelve.open("accounts", 'c') as db:
        accounts = db["accounts"]
        accounts[current_user.account_id].authenticated = False
        db["accounts"] = accounts

    logout_user()
    flash("You have logged out.")
    return redirect(url_for("admin_home"))


# API for updating account, to be called by Account Settings
@app.route("/admin/updateAccount", methods=["GET", "POST"])
@login_required
@admin_side
def admin_update_account():
    # TODO: Implement admin account soft-deletion

    if request.method == "GET":
        flash("fail")
        return redirect(url_for("admin_home"))

    # Check if current password entered was correct
    if not current_user.check_password_hash(request.form["updateSettingsPw"]):
        flash("Current Password is Wrong")
        return redirect(url_for("admin_home"))

    if "changeName" in request.form:
        if request.form["changeName"] != "":
            current_user.set_name(request.form["changeName"])
            flash("Successfully updated name to %s" % request.form[
                "changeName"])

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

    return redirect(url_for("admin_home"))


@app.route("/admin/deleteAccount")
@login_required
@admin_side
def delete_admin_account():
    # TODO: Add account settings password confirmation before allowing delete
    if current_user.is_authenticated:
        # current_user.hard_delete_account()
        with shelve.open(ACCOUNT_DB, 'c') as db:
            accounts = db["accounts"]
            account = accounts.get(current_user.account_id)
            account.disabled = True
            db["accounts"] = accounts

        flash("Successfully deleted your account")
    else:
        flash("Failed to delete your account!")

    return redirect(url_for("admin_logout"))


@app.route("/admin/coupon")
@login_required
@admin_side
def admin_coupon_management():
    # Get current CouponSystem from current_user (admin).
    coupon_system_id = current_user.coupon_system_id
    coupon_system = CouponSystem.query(coupon_system_id)
    coupon_list = coupon_system.get_coupons()
    count = len(coupon_list)

    return render_template("admin/retrieveCoupons.html",
                           coupon_list=coupon_list,
                           count=count)


@app.route("/admin/addCoupon", methods=["GET", "POST"])
@login_required
@admin_side
def admin_coupon_add():
    create_coupon_form = CreateCouponForm(request.form)

    if request.method == "POST" and create_coupon_form.validate():
        if create_coupon_form.expiry.data < date.today():
            flash("Date entered cannot be in the past!")
            return redirect(url_for("admin_coupon_add"))

        cs = CouponSystem.query(current_user.coupon_system_id)

        if create_coupon_form.discount_type.data == "fp":
            discount_type = CouponSystem.DISCOUNT_FIXED_PRICE
            discount_amount = float(create_coupon_form.discount_amount.data),
            discount_amount = discount_amount[0]  # for some reason we get a tuple here

            if discount_amount < 0:
                flash("Discount pricing can't be negative")
                return redirect(url_for("admin_coupon_add"))

        elif create_coupon_form.discount_type.data == "pct":
            discount_type = CouponSystem.DISCOUNT_PERCENTAGE_OFF
            discount_amount = float(create_coupon_form.discount_amount.data) / 100

            if discount_amount > 1:
                flash("Discount percentage can't be greater than 100%.")
                return redirect(url_for("admin_coupon_add"))

            if discount_amount < 0.01:
                flash("Discount percentage can't be less than 1%.")
                return redirect(url_for("admin_coupon_add"))
        else:
            flash("Invalid discount type!")
            return redirect(url_for("admin_coupon_add"))

        food_item_ids = create_coupon_form.food_item_ids.data.split()
        # Convert all item IDs entered to integers
        food_item_ids = [int(i) for i in food_item_ids]

        # TODO: Check if food item ids belong to the current restaurant.

        cs.new_coupon(create_coupon_form.coupon_code.data,
                      food_item_ids,
                      discount_type,
                      discount_amount,
                      create_coupon_form.expiry.data)

        return redirect(url_for("admin_coupon_management"))
    else:
        return render_template("admin/createCoupon.html", form=create_coupon_form)


@app.route("/admin/updateCoupon/<string:coupon_code>", methods=["GET", "POST"])
@login_required
@admin_side
def admin_coupon_update(coupon_code):
    cs = CouponSystem.query(current_user.coupon_system_id)
    coupon = cs.get_coupon(coupon_code)

    if not coupon:
        flash("Can't edit non-existent coupon with code %s" % coupon_code)
        return redirect(url_for("admin_coupon_management"))

    update_coupon_form = CreateCouponForm(request.form)

    if request.method == "POST" and update_coupon_form.validate():
        if update_coupon_form.expiry.data < date.today():
            flash("Date entered cannot be in the past!")
            return redirect(url_for("admin_coupon_management"))

        if update_coupon_form.discount_type.data == "fp":
            discount_type = CouponSystem.DISCOUNT_FIXED_PRICE
            discount_amount = float(update_coupon_form.discount_amount.data),
            discount_amount = discount_amount[0]  # for some reason we get a tuple here
        elif update_coupon_form.discount_type.data == "pct":
            discount_type = CouponSystem.DISCOUNT_PERCENTAGE_OFF
            discount_amount = float(update_coupon_form.discount_amount.data) / 100
        else:
            flash("Invalid discount type!")
            return redirect(url_for("admin_coupon_add"))

        food_item_ids = update_coupon_form.food_item_ids.data.split()
        food_item_ids = [int(i) for i in food_item_ids]

        # TODO: Check if food item ids belong to the current restaurant.

        cs.edit_coupon(coupon_code,
                       update_coupon_form.coupon_code.data,
                       food_item_ids,
                       discount_type,
                       discount_amount,
                       update_coupon_form.expiry.data)

        return redirect(url_for("admin_coupon_management"))

    discount_type = ""
    discount_amount = 0.0
    if coupon.discount.discount_type == CouponSystem.DISCOUNT_FIXED_PRICE:
        discount_type = "fp"
        discount_amount = coupon.discount.discount_amount
    elif coupon.discount.discount_type == CouponSystem.DISCOUNT_PERCENTAGE_OFF:
        discount_type = "pct"
        discount_amount = coupon.discount.discount_amount * 100

    food_items_str = ' '.join(str(i) for i in coupon.food_items)

    update_coupon_form.coupon_code.data = coupon.coupon_code
    update_coupon_form.food_item_ids.data = food_items_str
    update_coupon_form.discount_type.data = discount_type
    update_coupon_form.discount_amount.data = discount_amount
    update_coupon_form.expiry.data = coupon.expiry
    return render_template("admin/updateCoupon.html", form=update_coupon_form, coupon_code=coupon_code)


@app.route("/admin/deleteCoupon/<string:coupon_code>", methods=["GET", "POST"])
@login_required
@admin_side
def admin_coupon_delete(coupon_code):
    cs = CouponSystem.query(current_user.coupon_system_id)
    cs.delete_coupon(coupon_code)

    return redirect(url_for("admin_coupon_management"))


@app.route("/admin/testCoupon", methods=["POST"])
@login_required
@admin_side
def coupon_tester():
    cs = CouponSystem.query(current_user.coupon_system_id)
    food_id = int(request.form["foodID"])
    discount_code = request.form["discountCode"]

    try:
        dp = cs.discounted_price(food_id, discount_code)
    except FoodIdNotExistsError:
        flash("Food ID doesn't exist. You need to create it first.")
    else:
        flash("Discounted price is $%.2f" % dp)

    return redirect(url_for("admin_coupon_management"))


# Generate a random file name
def save_file(request_files, key: str):
    file = request_files[key]
    file_ext = os.path.splitext(file.filename)[1]
    filename = str(uuid.uuid4()) + str(file_ext)
    file_upload_path = os.path.join(os.getcwd(), "application/",
                                    app.config['UPLOAD_FOLDER'])
    os.makedirs(file_upload_path, exist_ok=True)
    filepath = os.path.join(file_upload_path, filename)
    file.save(filepath)
    stored_filename = "uploads/%s" % filename
    return stored_filename

# <---------------- Fixing the food management system ----------------->
MAX_SPECIFICATION_ID = 2  # for adding food
MAX_TOPPING_ID = 3


@app.route("/admin/menu")
@login_required
@admin_side
def admin_retrieve_food():
    food_list = FoodDao.get_foods(current_user.restaurant_id)
    return render_template('admin/food/retrieveFood.html', food_list=food_list)


def get_specs(request_form) -> list:
    specs = []

    # do specifications exist in first place?
    for i in range(MAX_SPECIFICATION_ID + 1):
        if "specification%d" % i in request_form:
            specs.append(request_form["specification%d" % i])
        else:
            break
    return specs


def get_toppings(request_form) -> list:
    toppings = []

    # do toppings exist in first place?
    for i in range(MAX_TOPPING_ID + 1):
        if "topping%d" % i in request_form:
            toppings.append(request_form["topping%d" % i])
        else:
            break
    return toppings


# Create food items. Rewritten by Ashlee.
@app.route('/admin/createFood', methods=['GET', 'POST'])
@login_required
@admin_side
def admin_create_food():
    create_food_form = CreateFoodForm(request.form)

    if request.method == 'POST' and create_food_form.validate():
        # Form submitted. Create a new food object here.
        restaurant_id = current_user.restaurant_id
        specs = get_specs(request.form)
        toppings = get_toppings(request.form)
        price = round(float(request.form["price"]), 2)

        # Handle the uploaded image here
        file = request.files["image"]


        # TODO: Validation for price

        # TODO: Add support for image
        stored_filename = save_file(request.files, "image")
        FoodDao.create_food(restaurant_id, name=request.form["name"], image=stored_filename,
                            description=request.form["description"],
                            price=price,
                            allergy=request.form["allergy"],
                            specifications=specs,
                            toppings=toppings)

        return redirect(url_for('admin_retrieve_food'))

    return render_template('admin/food/createFood.html', form=create_food_form,
                           MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                           MAX_TOPPING_ID=MAX_TOPPING_ID, )


@app.route("/admin/updateFood/<int:food_id>")
@login_required
@admin_side
def admin_update_food(food_id):
    update_food_form = CreateFoodForm(request.form)

    food = FoodDao.query(food_id)
    # Load the details of the food item.
    update_food_form.name = food.name
    return render_template('admin/food/createFood.html', form=update_food_form,
                           MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                           MAX_TOPPING_ID=MAX_TOPPING_ID, )


@app.route("/admin/deleteFood/<int:food_id>")
@login_required
@admin_side
def admin_delete_food(food_id):
    return "Placeholder %d" % food_id
