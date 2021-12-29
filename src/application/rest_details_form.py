from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import *


class RestaurantDetailsForm(Form):
    rest_name = StringField('Restaurant Name', [validators.Length(min=1, max=150), validators.DataRequired()])
