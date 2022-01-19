import datetime
import shelve
import traceback

from flask import render_template, request, redirect, url_for, session, flash
from flask_login import logout_user, login_required, current_user, login_user

from application import app
from application.CouponForms import CreateCouponForm
from application.Models.Admin import *
from application.Models.CouponSystem import CouponSystem
from application.rest_details_form import *

# <------------------------- ASHLEE ------------------------------>

@app.route("/admin")
@app.route("/admin/home", alias=True)
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
            accounts = db["accounts"]
            # For Flask-login
            accounts[account.account_id].authenticated = True
            db["accounts"] = accounts
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
    # Logout the current user
    current_user.authenticated = False
    with shelve.open("accounts", 'c') as db:
        accounts = db["accounts"]
        accounts[current_user.account_id].authenticated = False
        db["accounts"] = accounts

    logout_user()
    return redirect(url_for("admin_home"))


# API for updating account, to be called by Account Settings
@app.route("/admin/updateAccount", methods=["GET", "POST"])
@login_required
def admin_update_account():
    # TODO: Implement admin account soft-deletion

    if request.method == "GET":
        flash("fail")
        return redirect(url_for("admin_home"))

    # Check if current password entered was correct
    if not current_user.check_password_hash(request.form["updateSettingsPw"]):
        flash("Current Password is Wrong")
        return redirect(url_for("admin_home"))

    with shelve.open("accounts", 'c') as db:
        if "changeName" in request.form:
            if request.form["changeName"] != "":
                current_user.set_name(request.form["changeName"])
                flash("Successfully updated name to %s" % request.form["changeName"])

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
