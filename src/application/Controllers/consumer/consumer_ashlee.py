import functools
from datetime import datetime

from flask import url_for, render_template, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect

from application import app
from application.Models.Account import Account
from application.Models.Admin import Admin
from application.Models.Consumer import Consumer

# <------------------------- ASHLEE ------------------------------>

# Decorator to only allow consumer accounts or guests
from application.Models.FileUpload import save_file
from application.Models.RestaurantSystem import RestaurantSystem
from application.Models.Review import ReviewDao
from application.ReviewForms import CreateReviewForm


def consumer_side(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if isinstance(current_user, Consumer) or not current_user.is_authenticated:
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
            login.authenticate()
            login_user(login)
            return redirect(url_for("consumer_home"))
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
            for error in e.args:
                flash(str(error))
            return redirect(url_for("consumer_register"))

        account.authenticate()
        login_user(account)

        return redirect(url_for("consumer_home"))
    return render_template("consumer/account/register.html")


@app.route("/logout")
@login_required
@consumer_side
def consumer_logout():
    current_user.deauthenticate()
    logout_user()

    flash("You have logged out.")
    return redirect(url_for("consumer_home"))


@app.route('/writeReview', methods=["GET", "POST"])
@login_required
@consumer_side
def consumer_create_review():
    create_review_form = CreateReviewForm(request.form)
    list_of_restaurants = RestaurantSystem.get_restaurants()
    create_review_form.restaurant.choices += [(restaurant.id, restaurant.name) for restaurant in list_of_restaurants]

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

        ReviewDao.create_review(restaurant_id=create_review_form.restaurant.data,
                                reviewer_id=current_user.account_id,
                                stars=stars,
                                title=create_review_form.title.data,
                                description=create_review_form.description.data,
                                date_time=current_datetime,
                                media_path=media_path)
        # TODO: Redirect to My Reviews
        return redirect(url_for("consumer_retrieve_reviews"))

    return render_template("consumer/reviews/createReview.html", form=create_review_form)


@app.route("/myReviews")
@login_required
@consumer_side
def consumer_retrieve_reviews():
    list_of_reviews = ReviewDao.get_user_reviews(current_user.account_id)
    return render_template("consumer/reviews/myReviews.html", list_of_reviews=list_of_reviews,
                           count=len(list_of_reviews))


@app.route("/deleteReview/<int:review_id>")
@login_required
@consumer_side
def consumer_delete_review(review_id):
    ReviewDao.delete_review(review_id)
    return redirect(url_for("consumer_retrieve_reviews"))

@app.route('/cart')
@consumer_side
def consumer_cart():
    return render_template("consumer/cart.html")
