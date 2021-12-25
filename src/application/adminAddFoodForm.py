from wtforms import Form, StringField, TextAreaField, validators


class CreateFoodForm(Form):
    image = StringField('', [validators.Length(min=1, max=150),
                             validators.DataRequired()])

    item_name = StringField('', [validators.Length(min=1, max=10),
                                           validators.DataRequired()])

    description = TextAreaField('', [validators.Optional()])

    price = TextAreaField('', [validators.Optional()])

    allergy = TextAreaField('', [validators.Optional()])