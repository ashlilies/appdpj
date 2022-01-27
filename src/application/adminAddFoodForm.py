import decimal

from wtforms import Form, StringField, TextAreaField, DecimalField, validators, FileField
from wtforms.validators import DataRequired
from decimal import ROUND_HALF_UP

from application.BetterDecimalField import BetterDecimalField


class CreateFoodForm(Form):

    item_name = StringField('', [validators.Length(min=1, max=50),
                                 validators.DataRequired(message='Please enter the name of food!')])

    description = TextAreaField('', [validators.DataRequired(message='Description of food is required!')])

    price = BetterDecimalField('', places=2, round_always=True, rounding=ROUND_HALF_UP,
                               validators=[DataRequired(message='Price of food is required!')])

    # allergy = TextAreaField('', [validators.DataRequired()])

    allergy = TextAreaField('', [DataRequired(message="Enter Your Name Please")])
    image = FileField('')
