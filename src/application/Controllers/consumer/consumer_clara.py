from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from application import app

# <------------------------- CLARA ------------------------------>
from application.Controllers.admin.admin_ashlee import admin_side
from application.Controllers.consumer.consumer_ashlee import consumer_side
from application.Models.Food2 import FoodDao

#
from application.Models.RestaurantSystem import RestaurantSystem


# @app.route('/foodModal', methods=['GET', 'POST'])
# # @login_required
# # @admin_side
# def foodModal():
#     restaurants = RestaurantSystem.get_restaurants()
#     return render_template('consumer/foodModal.html',
#                            restaurants=restaurants, count=len(restaurants))


@app.route("/foodModal/<int:food_id>")
#displaying of food
@consumer_side
@login_required
def consumer_retrieve_food_modal(food_id):
    #retrieve the food created from FoodDao
    #using the currernt users restaurant_id
    food = FoodDao.query(food_id)
    return render_template('consumer/foodModal.html', food=food)




# def edit_user(id):
#     user = FoodDao.objects(id=id).first()
#     form = EditUserForm(obj=user)
#
#     if form.validate_on_submit() and request.method == 'POST':
#         user.first_name=form.first_name.data
#         user.last_name=form.last_name.data
#         user.email=form.email.data
#         user.roles = []
#
#         for role in form.roles.data:
#             r = Role.objects(name=role).first()
#             user.set_role(r.id)
#
#         if form.password.data:
#             user.set_password(form.password.data)
#
#         user.save()
#         return redirect(url_for('users'))
#
#     return render_template('edit_user.html', title='Edit user', user=user, form=form)
