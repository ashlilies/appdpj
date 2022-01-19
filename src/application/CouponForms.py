from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import *


class CreateCouponForm(Form):
    coupon_code = StringField('Coupon Code', [validators.Length(min=1, max=150), validators.DataRequired()])
    food_items = StringField('Food Items', [validators.Length(min=1, max=150), validators.DataRequired()])
    discount_type = SelectField('Discount Type', [validators.DataRequired()],
                         choices=[('', 'Select'), ('fp', 'Fixed Price'), ('pct', 'Percentage Off')], default='')
    discount_amount = DecimalField("Discount Amount", [validators.DataRequired()])
    expiry = DateTimeField('Expiry', [validators.DataRequired()])
