from wtforms import Form, StringField, SelectField, TextAreaField, validators


class CreateFoodForm(Form):
    image = StringField('', [validators.Length(min=1, max=150),
                             validators.DataRequired()])

    item_name = StringField('Dish name:', [validators.Length(min=1, max=10),
                                           validators.DataRequired()])

    description = TextAreaField('description:', [validators.Optional()])

    price = TextAreaField('price:', [validators.Optional()])

    allergy = TextAreaField('allergy:', [validators.Optional()])

    specification = SelectField('specification:', [validators.DataRequired()],
                                choices=[('', 'Select'), ('B', 'Beef'),
                                         ('V', 'Vegetarian')], default='')
