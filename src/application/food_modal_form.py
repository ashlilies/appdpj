#
# from flask_wtf import FlaskForm
# from wtforms import SelectMultipleField, SubmitField, TextAreaField, validators
# from flask_login import logout_user, login_required, current_user
# from application.Models.Food2 import FoodDao
#
#
#  class CustomiseForm(form):
#
#      request = TextAreaField('')
#
#      choices = []
#      food_list = FoodDao.get_cart_items(current_user.restaurant_id)
#      for food in food_list:
#          choices.append((food.name, food.topping))
#
#
#      roles = SelectMultipleField('Toppings', choices=choices)
#      submit = SubmitField('Save')
