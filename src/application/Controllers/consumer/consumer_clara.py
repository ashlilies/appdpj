from flask import render_template
from flask_login import login_required, current_user

from application import app

# <------------------------- CLARA ------------------------------>
from application.Controllers.admin.admin_ashlee import admin_side
from application.Models.Food2 import FoodDao

#
# @app.route('/consumer/foodModal', methods=['GET', 'POST'])
# # @login_required
# # @admin_side
# def foodModal():
#
#     return render_template('consumer/deliveryFoodMenu.html')

@app.route("/consumer/foodModal")
#displaying of food
@login_required
@admin_side
def consumer_retrieve_food_modal():
    #retrieve the food created from FoodDao
    #using the currernt users restaurant_id
    food_list = FoodDao.get_foods(current_user.restaurant_id)
    return render_template('consumer/deliveryFoodMenu.html', food_list=food_list)