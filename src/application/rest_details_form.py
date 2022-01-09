from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import *


class RestaurantDetailsForm(Form):
    rest_name = StringField('Restaurant Name', [validators.Optional()])
    rest_contact = IntegerField('Contact Number', [validators.Optional()])
    rest_hour_open = TimeField('Opening Hours:', [validators.Optional()])
    rest_hour_close = TimeField(' ', [validators.Optional()])
    rest_address1 = StringField('Address line 1', [validators.Optional()])
    rest_address2 = StringField('Address line 2', [validators.Optional()])
    rest_postcode = StringField('Postal Code', [validators.Optional()])
    rest_desc = TextAreaField('Restaurant Description:', [validators.Optional()])
    rest_bank = StringField('Bank Account', [validators.Optional()])
    rest_del1 = DecimalField('1-2km:', [validators.Optional()])
    rest_del2 = DecimalField('2-4km:', [validators.Optional()])
    rest_del3 = DecimalField('4-6km:', [validators.Optional()])
    rest_del4 = DecimalField('6-8km:', [validators.Optional()])
    rest_del5 = DecimalField('>9km:', [validators.Optional()])
