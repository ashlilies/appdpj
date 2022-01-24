import datetime
import traceback

import flask
from flask import render_template, request, redirect, url_for, session, flash, \
    Flask
from flask_login import logout_user, login_required, current_user
import os
import os.path

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
from application.Models.RestaurantSystem import *
import shelve, os
import uuid
from application.rest_details_form import *

# Ruri's imported libraries
import urllib.request
import os
from werkzeug.utils import secure_filename


# <------------------------- RURI ------------------------------>
# C (Create)
@app.route('/admin/create-restaurant', methods=['GET', 'POST'])
@login_required
def admin_myrestaurant():  # ruri
    restaurant_details_form = RestaurantDetailsForm(
        request.form)  # Using the Create Restaurant Form
    # The controller will be the place where we do all the interaction
    if request.method == 'POST' and restaurant_details_form.validate():
        # Checks if a restaurant has already been created by the current admin
        if not current_user.restaurant_id:

            #  The Below code is using one of the controller's method
            #  "Create_restaurant"
            # It's passing in the form argument to instantiate the restaurant
            # object
            # hygiene = request.files['hygieneDocument']
            # hygieneFile = secure_filename(hygiene.filename)
            # os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_PDF'])), exist_ok=True)
            # hygiene.save(os.path.join(os.getcwd(), app.config[
            #     'UPLOADED_PDF']) + hygieneFile)
            # logging.info('Hygiene -- file uploaded successfully')
            # save_hygiene = f"application/static/restaurantCertification/{restaurant_id}/{hygieneFile}"

            # print(current_user.restaurant_id)
            restaurant = RestaurantSystem.create_restaurant(
                restaurant_details_form.rest_name.data,
                request.form.get("rest_logo"),
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
                restaurant_details_form.rest_del5.data,
            )
            current_user.restaurant_id = restaurant.id

        else:
            restaurant = RestaurantSystem.find_restaurant_by_id(current_user.restaurant_id)
            RestaurantSystem.edit_restaurant(
                restaurant,
                restaurant_details_form.rest_name.data,
                request.form.get("rest_logo"),
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
                restaurant_details_form.rest_del5.data,
            )

        # ashlee - attach restaurant_id to our current user
        # current_user.restaurant_id = restaurant_id
        # print(current_user.restaurant_id)
        # Certification.restaurant_id = restaurant_id
        # Food.restaurant_id = restaurant_id
        # print(Certification.restaurant_id)
        # print(restaurant_id)
        # print(Food.restaurant_id)
        # RestaurantSystem.get_restaurant_by_id(current_user.restaurant_id)

        # flask_login.current_user.restaurant = restaurant_id
        # Once done, it'll redirect to the home page
        return redirect(url_for('test_upload'))

    # Load current restaurant's variables if the restaurant created before.
    if current_user.restaurant_id is not None:
        restaurant = RestaurantSystem.find_restaurant_by_id(current_user.restaurant_id)
        restaurant_details_form.rest_name.data = restaurant.name
        restaurant_details_form.rest_contact.data = restaurant.contact
        restaurant_details_form.rest_hour_open.data = restaurant.open
        restaurant_details_form.rest_hour_close.data = restaurant.close
        restaurant_details_form.rest_address1.data = restaurant.add1
        restaurant_details_form.rest_address2.data = restaurant.add2
        restaurant_details_form.rest_postcode.data = restaurant.postc
        restaurant_details_form.rest_desc.data = restaurant.desc
        restaurant_details_form.rest_bank.data = restaurant.bank
        restaurant_details_form.rest_del1.data = restaurant.del1
        restaurant_details_form.rest_del2.data = restaurant.del2
        restaurant_details_form.rest_del3.data = restaurant.del3
        restaurant_details_form.rest_del4.data = restaurant.del4
        restaurant_details_form.rest_del5.data = restaurant.del5

    return render_template("admin/restaurant.html",
                           form=restaurant_details_form,
                           restaurant=all_restaurant())


# R (Read)
# This is the route that displays all the relevant restaurant details
@app.route('/admin/my-restaurant')
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
        return render_template('admin/updateuserv2.html', form=edit_restaurant,
                               restaurant=restaurant)
    return render_template('admin/updateuserv2.html', form=edit_restaurant,
                           restaurant=all_restaurant())


# U (Update)
@app.route('/updateRestaurantConfirm/<id>', methods=['GET', 'POST'])
def update_restaurant_confirm(id):
    edit_restaurant = RestaurantDetailsForm(request.form)
    editing_restaurant = RestaurantSystem()
    if request.method == 'POST' and edit_restaurant.validate():
        editing_restaurant.edit_restaurant(
            id,
            edit_restaurant.rest_name.data,
            request.form.get("rest_logo"),
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


@app.route("/admin/dashboard")
def dashboard():  # ruri
    return render_template("admin/dashboard.html")
