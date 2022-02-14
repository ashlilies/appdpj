import functools
import logging
from datetime import datetime

from flask import render_template, session, request, redirect, url_for, flash, \
    current_app, make_response
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
from application.Models.Transaction import TransactionDao
from application.ReviewForms import CreateReviewForm
import stripe

# <------------------------- RURI ------------------------------>

publishable_key = 'pk_test_VrWD12lh918aMAaU4HP11c4e00I9shY8fg'
stripe.api_key = 'sk_test_kpzk6dqINLVhzC75dZi29d7z00bIiWFNxf'


@app.route("/payment", methods=['GET', 'POST'])
@consumer_side
@login_required
def payment():
    if request.method == "POST":
        cart = CartDao.get_cart(current_user.cart)

        customer = stripe.Customer.create(
            email=request.form['stripeEmail'],
            source=request.form['stripeToken'],
        )

        charge = stripe.Charge.create(
            customer='cus_L9F83gwhu37N0i',
            description='Foody pulse payment',
            amount=round(cart.get_subtotal() * 100),
            currency='sgd',
        )

        session["payment_made"] = True
        TransactionDao.create_transaction(cart.restaurant_id, current_user.account_id, cart.get_subtotal(), cart.coupon_code)

        return redirect(url_for('thankyou', restaurant_id=cart.restaurant_id))

    cart = CartDao.get_cart(current_user.cart)
    cart_items = cart.get_cart_items()
    return render_template("consumer/payment.html",
                           cart=cart,
                           cart_items=cart_items,
                           count=len(cart_items))


@app.route("/delordine")
@consumer_side
@login_required
def delordine():  # ruri
    return render_template('consumer/delOrDine.html')


@app.route("/thanks")
@consumer_side
@login_required
def thankyou():
    if session.get("payment_made"):
        cart = CartDao.get_cart(current_user.cart)
        cart.clear_cart()
        session["payment_made"] = False
    return render_template('consumer/thankyou.html')


# added by ashlee - load specific screens based on transaction status
@app.route("/thanks/<int:transaction_id>")
@consumer_side
@login_required
def transaction_confirmation(transaction_id):
    if session.get("payment_made"):
        cart = CartDao.get_cart(current_user.cart)
        cart.clear_cart()
        session["payment_made"] = False

    transaction = TransactionDao.get_transaction(transaction_id)
    return render_template('consumer/thanks.html', transaction=transaction)
