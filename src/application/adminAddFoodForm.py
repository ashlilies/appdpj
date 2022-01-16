from wtforms import Form, StringField, TextAreaField, DecimalField ,validators


class CreateFoodForm(Form):

    item_name = StringField('', [validators.Length(min=1, max=10),
                                           validators.DataRequired()])

    description = TextAreaField('', [validators.Optional()])

    price = DecimalField('', [validators.Optional()])

    allergy = TextAreaField('', [validators.Optional()])
    
    
    
    