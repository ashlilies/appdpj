import datetime
import traceback

import flask
from flask import render_template, request, redirect, url_for, session, flash, Flask
from flask_login import logout_user, login_required, current_user, login_user

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
def admin_myrestaurant():  # ruri
    restaurant_details_form = RestaurantDetailsForm(request.form)  # Using the Create Restaurant Form
    create_restaurant = RestaurantSystem()  # Creating a controller /
    # The controller will be the place where we do all the interaction
    if request.method == 'POST' and restaurant_details_form.validate():
        #  The Below code is using one of the controller's method
        #  "Create_restaurant"
        # It's passing in the form argument to instantiate the restaurant object
        restaurant_id = uuid.uuid4().hex
        current_user.restaurant_id = restaurant_id
        # print(current_user.restaurant_id)
        create_restaurant.create_restaurant(
            restaurant_id,
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
        session["rest_name"] = restaurant_details_form.rest_name.data
        session["rest_contact"] = restaurant_details_form.rest_name.data
        session["rest_hour_open"] = restaurant_details_form.rest_name.data
        session["rest_hour_close"] = restaurant_details_form.rest_name.data
        session["rest_address1"] = restaurant_details_form.rest_name.data
        session["rest_address2"] = restaurant_details_form.rest_name.data
        session["rest_postcode"] = restaurant_details_form.rest_name.data
        session["rest_desc"] = restaurant_details_form.rest_name.data
        session["rest_bank"] = restaurant_details_form.rest_name.data
        session["rest_del1"] = restaurant_details_form.rest_name.data
        session["rest_del2"] = restaurant_details_form.rest_name.data
        session["rest_del3"] = restaurant_details_form.rest_name.data
        session["rest_del4"] = restaurant_details_form.rest_name.data
        session["rest_del5"] = restaurant_details_form.rest_name.data
        # print(session["rest_name"])
        # print(restaurant_id)
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


