# xu yong lin
from wtforms import Form, validators, TextAreaField, SelectField


class ConsumerAddressForm(Form):
    # addressType = SelectField('Restaurant', choices=[('', '---'), (1, 'Home'), (2, 'Workplace'), (3, '3: Others')])
    # addressType = SelectField('Select your address', choices=[(1, '1: Home'), (2, '2: Work Address'), (3, '3: Others')])
    consumer_address = TextAreaField('Address', [validators.Optional(), validators.DataRequired()])
