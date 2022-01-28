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
from application.Models.Food import Food
from application.Models.Restaurant import Restaurant
from application import app, login_manager
from application.Models.Transaction import Transaction
from application.CreateFoodForm import CreateFoodForm
from werkzeug.utils import secure_filename
import shelve, os
import uuid
from application.rest_details_form import *



# <------------------------- CLARA ------------------------------>
MAX_SPECIFICATION_ID = 2  # for adding food
MAX_TOPPING_ID = 3

# APP ROUTE TO FOOD MANAGEMENT clara
# @app.route("/admin/foodManagement")
# def food_management():
#     create_food_form = CreateFoodForm(request.form)
#     # For the add food form
#
#     # food_dict = {}
#     # with shelve.open("food.db", "c") as db:
#     #     try:
#     #         if 'food' in db:
#     #             food_dict = db['food']
#     #         else:
#     #             db['food'] = food_dict
#     #     except Exception as e:
#     #         logging.error("create_food: error opening db (%s)" % e)
#
#     #--------------------------------------------------------------------
#
#     # food_dict = {}
#     # with shelve.open('food.db', 'c') as handle:
#     #     try:
#     #         if 'food.db' in handle:
#     #             food_dict = handle['food.db']
#     #             print('existing ', food_dict)
#     #             error = 'line 976 nothing wrong here'
#     #             print(error)
#     #             for key in food_dict:
#     #                 img = food_dict.get(key)
#     #                 print('img: ', img)
#     #             error2 = 'line 980 nothing wrong here'
#     #             print(error2)
#     #             # cert.hygiene_cert = f"application/static/restaurantCertification/hygiene/{cert.id}/"
#     #         else:
#     #             handle['food.db'] = food_dict
#     #             print(food_dict)
#     #             logging.info("food_management: nothing found in database, starting empty")
#     #     except Exception as e:
#     #         logging.error("food_management: error opening db (%s)" % e)
#
# #---------------------------------------------------------------------------------------
#     # storing the food keys in food_dict into a new list for displaying and
#     # deleting
#     food_list = []
#     # for key in food_dict:
#     #     food = food_dict.get(key)
#     #     food_list.append(food)
#
#
#     return render_template('admin/foodManagement.html',
#                            create_food_form=create_food_form,
#                            MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
#                            MAX_TOPPING_ID=MAX_TOPPING_ID,
#                            id=id,
#                            food_list=food_list)


# # ADMIN FOOD FORM clara
# @app.route('/admin/addFoodForm', methods=['GET', 'POST'])
# def create_food():
#     create_food_form = CreateFoodForm(request.form)
#
#     # get specifications as a List, no WTForms
#     def get_specs() -> list:
#         specs = []
#
#         # do specifications exist in first place?
#         for i in range(MAX_SPECIFICATION_ID + 1):
#             if "specification%d" % i in request.form:
#                 specs.append(request.form["specification%d" % i])
#             else:
#                 break
#
#         logging.info("create_food: specs is %s" % specs)
#         return specs
#
#         # get toppings as a List, no WTForms
#
#     def get_top() -> list:
#         top = []
#
#         # do toppings exist in first place?
#         for i in range(MAX_TOPPING_ID + 1):
#             if "topping%d" % i in request.form:
#                 top.append(request.form["topping%d" % i])
#             else:
#                 break
#
#         logging.info("create_food: top is %s" % top)
#         return top
#
#
#     # using the WTForms way to get the data
#     if request.method == 'POST' and create_food_form.validate():
#         food_dict = {}
#         # with shelve.open("food.db", "c") as db:
#         #     try:
#         #         if 'food' in db:
#         #             food_dict = db['food']
#         #
#         #         else:
#         #             db['food'] = food_dict
#         #     except Exception as e:
#         #         logging.error("create_food: error opening db (%s)" % e)
#
#         # Create a new food object
#         food = Food(request.form["image"], create_food_form.item_name.data,
#                     create_food_form.description.data,
#                     create_food_form.price.data,
#                     create_food_form.allergy.data)
#
#         test = 'line 142 nothing wrong here'
#         print(test)
#
#         food.set_specification(get_specs())  # set specifications as a List
#         food.topping = get_top()  # set topping as a List
#         food_dict[food.get_food_id()] = food  # set the food_id as key to store
#             # the food object
#             # db['food'] = food_dict
#
#             # # writeback
#             # with shelve.open("food.db", 'c') as db:
#             #     db['food'] = food_dict
#
#             # ---------------------------------------------------------------------------------------
#             #
#             # with shelve.open('food.db', 'c') as handle:
#             #     try:
#             #         food_dict = handle['food.db']
#             #         print(food_dict)
#             #     except Exception as e:
#             #         logging.error("createFood: ""food.db (%s)" % e)
#             #
#             #
#             #     img = Food()
#             #     app.config['UPLOADED_foodImages'] = f'application/static/foodImages/{img.id}/'
#             #     # print("931: %s" % halal)
#             #     f = request.files['foodImage']  # getting the file from the form
#             #     filename = secure_filename(f.filename)
#             #
#             #     os.makedirs(os.path.join(os.getcwd(), os.path.dirname(app.config['UPLOADED_foodImages'])),
#             #                 exist_ok=True)
#             #
#             #     # save document in app.config['UPLOAD_PDF']
#             #     f.save(os.path.join(os.getcwd(), app.config['UPLOADED_foodImages']) + filename)
#             #
#             #     logging.info('file uploaded successfully')
#             #
#             #
#             # # create new object
#             # img.food_image = f"application/static/foodImages/{img.id}/{filename}"
#             #
#             # # cert = Certification(f)
#             # food_dict[img.id] = img
#             # handle['food.db'] = food_dict
# # ---------------------------------------------------------------------------------------
#         return redirect(url_for('food_management'))
#
#     return render_template('admin/addFoodForm.html', form=create_food_form,
#                            MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
#                            MAX_TOPPING_ID=MAX_TOPPING_ID, )
#



# # Note from Ashlee: when doing integration, please prefix all URLs with /admin/
# @app.route('/deleteFood/<int:id>', methods=['POST'])
# def delete_food(id):
#     food_dict = {}
#     # with shelve.open("food.db", 'c') as db:
#     #     food_dict = db['food']
#     #     food_dict.pop(id)
#     #     db['food'] = food_dict
#
#     return redirect(url_for('food_management'))


# # Note from Ashlee: when doing integration, please prefix all URLs with /admin/
# # save new specification and list
# @app.route('/updateFood/<int:id>/', methods=['GET', 'POST'])
# def update_food(id):
#     update_food_form = CreateFoodForm(request.form)
#
#     # get specifications as a List, no WTForms
#     def get_specs() -> list:
#         specs = []
#
#         # do specifications exist in first place?
#         for i in range(MAX_SPECIFICATION_ID + 1):
#             if "specification%d" % i in request.form:
#                 specs.append(request.form["specification%d" % i])
#             else:
#                 break
#
#         logging.info("create_food: specs is %s" % specs)
#         return specs
#
#         # get toppings as a List, no WTForms
#
#     def get_top() -> list:
#         top = []
#
#         # do toppings exist in first place?
#         for i in range(MAX_TOPPING_ID + 1):
#             if "topping%d" % i in request.form:
#                 top.append(request.form["topping%d" % i])
#             else:
#                 break
#
#         logging.info("create_food: top is %s" % top)
#         return top
#
#     if request.method == 'POST' and update_food_form.validate():
#         food_dict = {}
#         try:
#             # with shelve.open("food.db", 'w') as db:
#             #     food_dict = db['food']
#             #     food = food_dict.get(id)
#                 food = Food.query(id)
#                 # food.set_image = request.form["image"]
#                 food.set_name(update_food_form.item_name.data)
#                 food.set_description(update_food_form.description.data)
#                 food.set_price(update_food_form.price.data)
#                 food.set_allergy(update_food_form.allergy.data)
#                 food.set_specification(get_specs())  # set specifications as a List
#                 food.toppings = get_top()  # set topping as a List
#                 # db["food"] = food_dict
#         except Exception as e:
#             logging.error("update_customer: %s" % e)
#             print("an error has occured in update customer")
#
#         return redirect("/admin/foodManagement")
#     else:
#         food_dict = {}
#         try:
#             # with shelve.open("food.db", 'r') as db:
#             #     food_dict = db['food']
#             #
#             #     food = food_dict.get(id)
#                 food = Food.query(id)
#
#                 # food.get_image(request.form["image"])
#                 update_food_form.item_name.data = food.get_name()
#                 update_food_form.description.data = food.get_description()
#                 update_food_form.price.data = food.get_price()
#                 update_food_form.allergy.data = food.get_allergy()
#
#                 # for food in food_dict:
#                 #     food.get_specification()
#                 #     food.get_topping()
#                 #
#         except:
#             print("Error occured when update food")
#
#         return render_template('admin/updateFood.html',
#                                form=update_food_form,
#                                food=food,
#                                MAX_SPECIFICATION_ID=MAX_SPECIFICATION_ID,
#                                MAX_TOPPING_ID=MAX_TOPPING_ID)
#
# @app.route('/updateFood/<int:id>/', methods=['GET', 'POST'])
#
# #save new specification and list
#
# def update_food(id):
#     update_food_form = CreateFoodForm(request.form)
#
#     # get specifications as a List, no WTForms
#     def get_specs() -> list:
#         specs = []
#
#         # do specifications exist in first place?
#         for i in range(MAX_SPECIFICATION_ID + 1):
#             if "specification%d" % i in request.form:
#                 specs.append(request.form["specification%d" % i])
#             else:
#                 break
#
#         logging.info("create_food: specs is %s" % specs)
#         return specs
#
#         # get toppings as a List, no WTForms
#
#     def get_top() -> list:
#         top = []
#
#         # do toppings exist in first place?
#         for i in range(MAX_TOPPING_ID + 1):
#             if "topping%d" % i in request.form:
#                 top.append(request.form["topping%d" % i])
#             else:
#                 break
#
#         logging.info("create_food: top is %s" % top)
#         return top
#
#
#     if request.method == 'POST' and update_food_form.validate():
#         food_dict = {}
#         with shelve.open("food.db", 'w') as db:
#             food_dict = db['food']
#
#             food = food_dict.get(id)
#             food.set_image(request.form["image"])
#             food.set_name(update_food_form.item_name.data)
#             food.set_description(update_food_form.description.data)
#             food.set_price(update_food_form.price.data)
#             food.set_allergy(update_food_form.allergy.data)
#             food.specification = get_specs()  # set specifications as a List
#             food.topping = get_top()  # set topping as a List
#
#             db['food'] = food_dict
#
#         return redirect(url_for('food_management'))
#     else:
#         food_dict = {}
#         with shelve.open("food.db", 'r') as db:
#             food_dict = db['food']
#
#         food = food_dict.get(id)
#         update_food_form.item_name.data = food.get_name()
#         update_food_form.description.data = food.get_description()
#         update_food_form.price.data = food.get_price()
#         update_food_form.allergy.data = food.get_allergy()
#         food.specification = get_specs()  # set specifications as a List
#         food.topping = get_top()  # set topping as a List
#
#         return render_template('admin/updateFood.html', form=update_food_form)
