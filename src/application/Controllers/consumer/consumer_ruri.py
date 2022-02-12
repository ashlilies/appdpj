import functools
import logging
from datetime import datetime

from flask import url_for, render_template, flash, request, session
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect

from application import app
from application.Controllers.consumer.consumer_ashlee import consumer_side
from application.Models.Account import Account
from application.Models.Admin import Admin
from application.Models.Cart import CartDao, Cart
from application.Models.Consumer import Consumer

# Decorator to only allow consumer accounts or guests
from application.Models.FileUpload import save_file
from application.Models.Food2 import FoodDao
from application.Models.RestaurantSystem import RestaurantSystem
from application.Models.Review import ReviewDao
from application.ReviewForms import CreateReviewForm
import stripe
# <------------------------- RURI ------------------------------>

publishable_key = 'pk_test_VrWD12lh918aMAaU4HP11c4e00I9shY8fg'
stripe.api_key = 'sk_test_kpzk6dqINLVhzC75dZi29d7z00bIiWFNxf'


@app.route("/payment")
@consumer_side
@login_required
def payment():
    cart = CartDao.get_cart(current_user.cart)
    cart_items = cart.get_cart_items()
    return render_template("consumer/payment.html",
                           cart=cart,
                           cart_items=cart_items,
                           count=len(cart_items))
    return redirect(url_for('thankyou'))

@app.route("/delordine")
@consumer_side
@login_required
def delordine():  # ruri
    return render_template('consumer/delOrDine.html')

@app.route("/thanks")
@consumer_side
@login_required
def thankyou():
    return render_template('customer/thankyou.html')


