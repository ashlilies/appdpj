import datetime
import traceback

import flask
from flask import render_template, request, redirect, url_for, session, flash, Flask
from flask_login import logout_user, login_required, current_user
import os
import os.path

from application.CouponForms import CreateCouponForm
from application.Models.Admin import *
from application.Models.CouponSystem import CouponSystem
from application.Models.Certification import Certification
from application.Models.FileUpload import save_file
from application.Models.Food import Food
from application.Models.Restaurant import Restaurant
from application import app, login_manager
from application.Models.Transaction import Transaction
from application.adminAddFoodForm import CreateFoodForm

from werkzeug.utils import secure_filename
import shelve, os
import uuid
from application.rest_details_form import *


# <------------------------- CLARA ------------------------------>
@app.route("/admin/foodManagement")
def food_management():
    create_food_form = CreateFoodForm(request.form)
    food_dict = {}
    with shelve.open("food.db", "c") as db:
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
    for key in food_dict:  # the keys will be the food_id
        food = food_dict.get(key)
        food_list.append(food)

    return render_template('admin/foodManagement.html',
                           create_food_form=create_food_form,
                           MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                           MAX_TOPPING_ID=MAX_TOPPING_ID,
                           id=id,
                           food_list=food_list)


MAX_SPECIFICATION_ID = 2  # for adding food
MAX_TOPPING_ID = 3

app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'


# ADMIN FOOD FORM clara
@app.route('/admin/foodManagement', methods=['GET', 'POST'])

def create_food():
    create_food_form = CreateFoodForm(request.form)
    # get specifications as a List, no WTForms
    def get_specs() -> list:  # tells that the function will return a list, python ignores it
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
            # check in request.form if there is any toppings added
            # (the name of topping field is topping%d in the html javascript)
            if "topping%d" % i in request.form:
                # retrieve the data if have then append
                top.append(request.form["topping%d" % i])
            else:
                break

        logging.info("create_food: top is %s" % top)
        return top

    # using the WTForms way to get the data
    # usually the method is GET but when its form its POST
    # so if the method is POST and the form is validated
    if request.method == 'POST' and create_food_form.validate():
        food_dict = {}
        # open shelve and create the object with the data inputted
        with shelve.open("food.db", "c") as db:
            try:
                if 'food' in db:
                    food_dict = db['food']

                else:
                    db['food'] = food_dict
            except Exception as e:
                logging.error("create_food: error opening db (%s)" % e)

            stored_filename = save_file(request.files, "image_file")
            # Create a new food object (parse in the data inputted)
            food = Food(stored_filename, create_food_form.item_name.data,
                        create_food_form.description.data,
                        create_food_form.price.data,
                        create_food_form.allergy.data)
            # set specifications as a List and appeded
            # as an attribute for that food object
            food.specification = get_specs()
            food.topping = get_top()  # set topping as a List
            # set the food_id as key to store
            # the food object
            food_dict[food.get_food_id()] = food
            db['food'] = food_dict

            # writeback so changes are "updated"
            with shelve.open("food.db", 'c') as db:
                db['food'] = food_dict

            return redirect(url_for('food_management'))

    return render_template('admin/foodManagement.html',
                           form=create_food_form,
                           MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                           MAX_TOPPING_ID=MAX_TOPPING_ID)



# Note from Ashlee: when doing integration, please prefix all URLs with /admin/
@app.route('/deleteFood/<int:id>', methods=['POST'])
def delete_food(id):
    with shelve.open("food.db", 'c') as db:
        food_dict = db['food']
        food_dict.pop(id)
        db['food'] = food_dict

    return redirect(url_for('food_management'))


# Note from Ashlee: when doing integration, please prefix all URLs with /admin/
# save new specification and list
@app.route('/updateFood/<int:id>/', methods=['GET', 'POST'])
def update_food(id):
    # parsing in the data inputted by user request.form
    # into the createFoodForm class
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
            #open shelve and set the attributes to the new values
            with shelve.open("food.db", 'w') as db:
                food_dict = db['food']
                food = food_dict.get(id)
                # food.set_image = request.form["image"]
                stored_filename = save_file(request.files, "image_file")
                food.set_image(stored_filename)
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
            # open shelve, retrive the inputted
            # values and display it in the field
            with shelve.open("food.db", 'r') as db:
                food_dict = db['food']
                food = food_dict.get(id)
                update_food_form.test.data = food.get_image()
                update_food_form.item_name.data = food.get_name()
                update_food_form.description.data = food.get_description()
                update_food_form.price.data = food.get_price()
                update_food_form.allergy.data = food.get_allergy()


        except:
            print("Error occured when update food")

        return render_template('admin/updateFood.html',
                               form=update_food_form,
                               food=food,
                               MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
                               MAX_TOPPING_ID=MAX_TOPPING_ID)
