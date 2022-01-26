# Ashlee

from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import StringField, SelectField, DecimalField, DateField


class CreateCouponForm(Form):
    coupon_code = StringField('Coupon Code', [validators.Length(min=1, max=150), validators.DataRequired()])
    food_item_ids = StringField('Food Item IDs (space separated)', [validators.Length(min=1, max=150), validators.DataRequired()])
    discount_type = SelectField('Discount Type', [validators.DataRequired()],
                         choices=[('', 'Select'), ('fp', 'Fixed Price'), ('pct', 'Percentage Off')], default='')
    discount_amount = DecimalField("Discount Amount", [validators.DataRequired()])

    # DateTimeLocalField doesn't work in Firefox, only Chrome. Hence separate.
    expiry = DateField('Expiry Date', [validators.DataRequired()])
