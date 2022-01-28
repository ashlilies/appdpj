import datetime
import traceback

import flask
from flask import render_template, request, redirect, url_for, session, flash, \
    Flask
from flask_login import logout_user, login_required, current_user
import os
import os.path

from application.Controllers.admin.admin_ashlee import admin_side
from application.CouponForms import CreateCouponForm
from application.Models.Admin import *
from application.Models.CouponSystem import CouponSystem
from application.Models.Certification import Certification
from application.Models.FileUpload import save_file
from application.Models.Food import Food
from application.Models.Food2 import FoodDao
from application.Models.Restaurant import Restaurant
from application import app, login_manager
from application.Models.Review import ReviewDao
from application.Models.Transaction import Transaction
from application.CreateFoodForm import CreateFoodForm
from werkzeug.utils import secure_filename
import shelve, os
import uuid
from application.rest_details_form import *

# <------------------------- CLARA ------------------------------>
MAX_SPECIFICATION_ID = 2  # for adding food
MAX_TOPPING_ID = 3


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

        # TODO: Validation for price

        # TODO: Add support for image
        stored_filename = save_file(request.files, "image")
        FoodDao.create_food(restaurant_id, name=request.form["name"],
                            image=stored_filename,
                            description=request.form["description"],
                            price=price,
                            allergy=request.form["allergy"],
                            specifications=specs,
                            toppings=toppings)

        return redirect(url_for('admin_retrieve_food'))

    return render_template('admin/food/createFood.html', form=create_food_form,
                           MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                           MAX_TOPPING_ID=MAX_TOPPING_ID, )


@app.route("/admin/menu")
@login_required
@admin_side
def admin_retrieve_food():
    food_list = FoodDao.get_foods(current_user.restaurant_id)
    return render_template('admin/food/retrieveFood.html', food_list=food_list)


@app.route("/admin/updateFood/<int:food_id>", methods=["GET", "POST"])
@login_required
@admin_side
def admin_update_food(food_id):
    update_food_form = CreateFoodForm(request.form)
    food = FoodDao.query(food_id)

    if request.method == "POST" and update_food_form.validate():
        image_path = food.image
        if request.files["image"].filename != "":  # file was uploaded
            image_path = save_file(request.files, "image")

        specs = get_specs(request.form)
        toppings = get_toppings(request.form)
        price = round(float(request.form["price"]), 2)

        # TODO: Validation for price

        FoodDao.update_food(food_id=food.id, name=request.form["name"],
                            image_path=image_path,
                            description=request.form["description"],
                            price=price, allergy=request.form["allergy"],
                            specification=specs,
                            topping=toppings)

        return redirect(url_for("admin_retrieve_food"))

    # Load the details of the food item.
    update_food_form.name.data = food.name
    update_food_form.description.data = food.description
    update_food_form.price.data = food.price
    update_food_form.allergy.data = food.allergy

    return render_template('admin/food/updateFood.html',
                           form=update_food_form,
                           food_id=food_id,
                           MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                           MAX_TOPPING_ID=MAX_TOPPING_ID)


@app.route("/admin/deleteFood/<int:food_id>")
@login_required
@admin_side
def admin_delete_food(food_id):
    FoodDao.delete_food(food_id)
    return redirect(url_for("admin_retrieve_food"))
