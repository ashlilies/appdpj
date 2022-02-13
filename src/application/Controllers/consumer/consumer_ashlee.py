import functools
import logging
import traceback
from datetime import datetime

from flask import url_for, render_template, flash, request, session
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect

from application import app
from application.Models.Account import Account
from application.Models.Admin import Admin
from application.Models.Cart import CartDao, Cart
from application.Models.Consumer import Consumer

# <------------------------- ASHLEE ------------------------------>

# Decorator to only allow consumer accounts or guests
from application.Models.FileUpload import save_file
from application.Models.Food2 import FoodDao
from application.Models.RestaurantSystem import RestaurantSystem
from application.Models.Review import ReviewDao
from application.ReviewForms import CreateReviewForm


def consumer_side(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if isinstance(current_user,
                      Consumer) or not current_user.is_authenticated:
            print(current_user)
            return view(*args, **kwargs)
        flash("You need to log out first to access the Consumer side.")
        return redirect('/admin')

    return wrapper


@app.route('/')
@app.route("/consumer", alias=True)
@consumer_side
def consumer_home():
    return render_template("consumer/home.html")


@app.route('/login', methods=["GET", "POST"])
@consumer_side
def consumer_login():
    def login_error():
        return redirect("%s?error=1" % url_for("consumer_login"))

    if request.method == "POST":
        login = Account.check_credentials(request.form["email"],
                                          request.form["password"])
        if login is not None:
            if login.check_otp(request.form["otp"]):
                login.authenticate()
                login_user(login)
                return redirect(url_for("consumer_home"))
            else:
                flash("Incorrect OTP")
                return render_template("consumer/account/login.html")
        return login_error()

    return render_template("consumer/account/login.html")


@app.route("/register", methods=["GET", "POST"])
@consumer_side
def consumer_register():
    if request.method == "POST":
        # TODO: Validate input manually to prevent hacks?
        pw1 = request.form["password"]
        pw2 = request.form["passwordAgain"]

        if pw1 != pw2:
            flash("Passwords don't match")
            return redirect(url_for("consumer_register"))

        try:
            account = Consumer(first_name=request.form["firstName"],
                               last_name=request.form["lastName"],
                               email=request.form["email"],
                               password=request.form["password"])
        except Exception as e:
            flash("An error occured. Please contact FoodyPulse support.")
            traceback.print_exc()
            return redirect(url_for("consumer_register"))

        account.authenticate()
        login_user(account)

        flash("Your OTP secret is %s. Enter this into your OTP app!"
              % account.totp_secret)
        return redirect(url_for("consumer_home"))
    return render_template("consumer/account/register.html")


# Generic logout for all account types
@app.route("/logout")
@login_required
def logout():
    if isinstance(current_user, Admin):
        redirect_url = url_for("admin_home")
    else:
        redirect_url = url_for("consumer_home")

    current_user.deauthenticate()
    logout_user()

    flash("You have logged out.")
    return redirect(redirect_url)


@app.route('/writeReview', methods=["GET", "POST"])
@login_required
@consumer_side
def consumer_create_review():
    create_review_form = CreateReviewForm(request.form)
    list_of_restaurants = RestaurantSystem.get_restaurants()
    create_review_form.restaurant.choices += [(restaurant.id, restaurant.name)
                                              for restaurant in
                                              list_of_restaurants]

    if request.method == "POST" and create_review_form.validate():
        # Check that restaurant and stars are not invalid
        if create_review_form.restaurant.data == "":
            flash("Please choose a restaurant to review!")
            return redirect(url_for("consumer_create_review"))

        if create_review_form.stars.data == "":
            flash("Please choose a number of stars!")
            return redirect(url_for("consumer_create_review"))

        current_datetime = datetime.now()
        stars = int(create_review_form.stars.data)
        media_path = ""
        if request.files[create_review_form.media.name].filename != "":
            media_path = save_file(request.files, create_review_form.media.name)

        ReviewDao.create_review(
            restaurant_id=create_review_form.restaurant.data,
            reviewer_id=current_user.account_id,
            stars=stars,
            title=create_review_form.title.data,
            description=create_review_form.description.data,
            date_time=current_datetime,
            media_path=media_path)
        # TODO: Redirect to My Reviews
        return redirect(url_for("consumer_retrieve_reviews"))

    return render_template("consumer/reviews/createReview.html",
                           form=create_review_form)


@app.route("/myReviews")
@login_required
@consumer_side
def consumer_retrieve_reviews():
    list_of_reviews = ReviewDao.get_user_reviews(current_user.account_id)
    return render_template("consumer/reviews/myReviews.html",
                           list_of_reviews=list_of_reviews,
                           count=len(list_of_reviews))


@app.route("/deleteReview/<int:review_id>")
@login_required
@consumer_side
def consumer_delete_review(review_id):
    ReviewDao.delete_review(review_id)
    return redirect(url_for("consumer_retrieve_reviews"))


# TODO: Identify ordering type, handle discounts
@app.route('/cart')
@login_required
@consumer_side
def consumer_cart():
    cart = CartDao.get_cart(current_user.cart)
    cart_items = cart.get_cart_items()
    return render_template("consumer/cart.html",
                           cart=cart,
                           cart_items=cart_items,
                           count=len(cart_items))


# GET for manipulating the quantity buttons, POST for adding a customized one.
@app.route("/cart/add/<int:food_id>", methods=["GET", "POST"])
@login_required
@consumer_side
def cart_add(food_id):
    if session["cart_mode"] != Cart.NOT_SET:
        cart = CartDao.get_cart(current_user.cart)

        if request.method == "POST":
            topping_list = []
            food = FoodDao.query(food_id)
            for topping in food.toppings:
                checked = request.form.get(topping)
                if checked is not None:
                    topping_list.append(topping)

            custom_requests = request.form["otherRequest"]
        else:
            cart_item_dict = cart.get_cart_items_dict()
            topping_list = cart_item_dict[food_id].toppings
            custom_requests = cart_item_dict[food_id].requests

        cart.add_item(food_id, 1, topping_list, custom_requests)
        cart.mode = session["cart_mode"]
        flash("Successfully added item to cart")
    else:
        flash("Error adding item to cart")
        logging.error("Couldn't add item to cart due to unset mode")

    return redirect(url_for("consumer_cart"))


# For removing a quantity of an item
@app.route("/cart/del/<int:food_id>")
@login_required
@consumer_side
def cart_del(food_id):
    cart = CartDao.get_cart(current_user.cart)
    cart.remove_item(food_id)
    if cart.is_empty():
        return redirect(url_for("cart_clear"))

    flash("Successfully removed item from cart")

    return redirect(url_for("consumer_cart"))


# For removing ALL of an item.
@app.route("/cart/delItem/<int:food_id>")
@login_required
@consumer_side
def cart_del_item(food_id):
    cart = CartDao.get_cart(current_user.cart)
    cart.remove_item(food_id, remove_all=True)
    if cart.is_empty():
        return redirect(url_for("cart_clear"))

    flash("Successfully removed item from cart")

    return redirect(url_for("consumer_cart"))


@app.route("/cart/clear")
@login_required
@consumer_side
def cart_clear():
    cart = CartDao.get_cart(current_user.cart)
    cart.clear_cart()
    cart.mode = Cart.NOT_SET
    cart.apply_coupon("")  # clear the coupon to prevent bugs
    flash("Successfully emptied the cart")

    return redirect(url_for("consumer_cart"))


@app.route("/dineIn")
@consumer_side
@login_required
def dine_in():
    cart = CartDao.get_cart(current_user.cart)
    if not (cart.mode == Cart.DINE_IN or cart.mode == Cart.NOT_SET):
        flash("You are already placing a Delivery order. "
              "Complete it first, or empty your cart.")
        return redirect(url_for("delivery"))

    restaurants = RestaurantSystem.get_restaurants()
    return render_template("consumer/dineIn/dineIn.html",
                           restaurants=restaurants, count=len(restaurants))


@app.route("/dineIn/<string:restaurant_id>")
@consumer_side
@login_required
def dine_in_food(restaurant_id):
    session["cart_mode"] = Cart.DINE_IN

    restaurant = RestaurantSystem.find_restaurant_by_id(restaurant_id)
    food_list = FoodDao.get_foods(restaurant_id)

    if restaurant is None:
        return redirect(url_for("delivery"))

    return render_template("consumer/dineIn/dineInMenu.html",
                           restaurant=restaurant, food_list=food_list,
                           count=len(food_list))


@app.route("/delivery")
@consumer_side
@login_required
def delivery():
    cart = CartDao.get_cart(current_user.cart)
    if not (cart.mode == Cart.DELIVERY or cart.mode == Cart.NOT_SET):
        flash("You are already placing a Dine-In order. "
              "Complete it first, or empty your cart.")
        return redirect(url_for("dine_in"))

    restaurants = RestaurantSystem.get_restaurants()
    return render_template("consumer/delivery/delivery_tmp.html",
                           restaurants=restaurants, count=len(restaurants))


@app.route("/delivery/<string:restaurant_id>")
@consumer_side
@login_required
def delivery_food(restaurant_id):
    session["cart_mode"] = Cart.DELIVERY

    restaurant = RestaurantSystem.find_restaurant_by_id(restaurant_id)
    food_list = FoodDao.get_foods(restaurant_id)

    if restaurant is None:
        return redirect(url_for("delivery"))

    return render_template("consumer/delivery/deliveryMenu_tmp.html",
                           restaurant=restaurant, food_list=food_list,
                           count=len(food_list))


@app.route("/applyCoupon", methods=["POST"])
@consumer_side
@login_required
def apply_coupon():
    if "couponCode" in request.form:
        coupon_code = request.form["couponCode"]

        # apply coupon to the current Cart
        cart = CartDao.get_cart(current_user.cart)
        cart.apply_coupon(request.form["couponCode"])

        if coupon_code == "":
            flash("Successfully removed coupon code from cart")
        elif cart.get_total_discount() == 0.0:
            flash("Invalid coupon code - either items are not applicable, "
                  "or code doesn't exist!")
            cart.apply_coupon("")  # blank it
        else:
            flash("Successfully applied coupon!")

    return redirect(url_for("consumer_cart"))


# API for updating account, to be called by Account Settings
@app.route("/updateAccount", methods=["GET", "POST"])
@login_required
@consumer_side
def consumer_update_account():
    if request.method == "GET":
        flash("Failed to update account settings")
        return redirect(url_for("consumer_home"))

    # Check if current password entered was correct
    if not current_user.check_password_hash(request.form["updateSettingsPw"]):
        flash("Current Password is Wrong")
        return redirect(url_for("consumer_home"))

    if "changeFirstName" in request.form:
        if request.form["changeFirstName"] != "":
            current_user.first_name = request.form["changeFirstName"]
            current_user.save()
            flash("Successfully updated First Name to %s"
                  % request.form["changeFirstName"])

    if "changeLastName" in request.form:
        if request.form["changeLastName"] != "":
            current_user.last_name = request.form["changeLastName"]
            current_user.save()
            flash("Successfully updated Last Name to %s"
                  % request.form["changeLastName"])

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

    return redirect(url_for("consumer_home"))


@app.route("/forgetPassword", methods=["GET", "POST"])
@consumer_side
def consumer_forget_password():
    if request.method == "POST":
        email = request.form["email"]
        account = Account.get_account_by_email(email)
        if account is not None:
            flash("An email with a link has been sent.")
            account.reset_password()
            return redirect(url_for("consumer_forget_password_key"))
        else:
            flash("Email doesn't exist.")

    return render_template("consumer/account/forgetPassword.html")


@app.route("/forgetPasswordKey", methods=["GET", "POST"])
@consumer_side
def consumer_forget_password_key():
    if request.method == "POST":
        email = request.form["email"]
        account = Account.get_account_by_email(email)
        tok = request.form["token"]
        if account is not None:
            return redirect(url_for("password_auto_reset",
                                    account_id=account.account_id,
                                    pw_reset_token=tok))
        else:
            flash("Invalid email")
    return render_template("consumer/account/forgetPasswordKey.html")

# This endpoint works for all account types
@app.route("/<int:account_id>/<string:pw_reset_token>")
def password_auto_reset(account_id, pw_reset_token):
    account = Account.query(account_id)
    if account.reset_pw_verify(pw_reset_token):
        flash("A new password has been sent to your email.")

        if isinstance(Account.query(account_id), Admin):
            return redirect(url_for("admin_home"))
        else:
            return redirect(url_for("consumer_home"))

    flash("Wrong password reset key. Try again?")

    if isinstance(account, Admin):
        return redirect(url_for("admin_forget_password_key"))
    return redirect(url_for("consumer_forget_password_key"))

# Regenerate OTP for all account types
@app.route("/regenOTP")
@login_required
def regenerate_otp():
    current_user.generate_otp_secret()
    flash("Your OTP secret is %s. Enter this into your OTP app!"
          % current_user.totp_secret)

    if isinstance(current_user, Admin):
        return redirect(url_for("admin_home"))
    return redirect(url_for("consumer_home"))