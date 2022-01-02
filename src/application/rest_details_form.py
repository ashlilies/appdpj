from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import *
from wtforms_components import TimeField

class RestaurantDetailsForm(Form):
    rest_name = StringField('Restaurant Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    rest_contact = IntegerField('Contact Number', [validators.Length(min=1, max=8), validators.DataRequired()])
    rest_hour_open = TimeField('Opening Hours:', [validators.Length(min=1, max=150), validators.DataRequired()])
    rest_hour_close = TimeField(' ', [validators.Length(min=1, max=150), validators.DataRequired()])
    rest_address1 = StringField('Address line 1', [validators.Length(min=1, max=150), validators.DataRequired()])
    rest_address2 = StringField('Address line 2', [validators.Length(min=1, max=150), validators.DataRequired()])
    rest_postcode = StringField('Postal Code', [validators.Length(min=1, max=150), validators.DataRequired()])
    rest_desc = TextAreaField('Restaurant Description:', [validators.Length(min=1, max=200), validators.DataRequired()])
    rest_bank = StringField('Bank Account', [validators.Length(min=1, max=150), validators.DataRequired()])
    rest_del1 = DecimalField('1-2km:', [validators.Length(min=1, max=150), validators.DataRequired()])
    rest_del2 = DecimalField('2-4km:', [validators.Length(min=1, max=150), validators.DataRequired()])
    rest_del3 = DecimalField('4-6km:', [validators.Length(min=1, max=150), validators.DataRequired()])
    rest_del4 = DecimalField('6-8km:', [validators.Length(min=1, max=150), validators.DataRequired()])
    rest_del5 = DecimalField('>9km:', [validators.Length(min=1, max=150), validators.DataRequired()])
