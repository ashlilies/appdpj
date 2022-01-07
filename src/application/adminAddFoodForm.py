from wtforms import Form, StringField, TextAreaField, validators


class CreateFoodForm(Form):

    def __init__(
            self,
            formdata=None,
            obj=None,
            prefix="",
            data=None,
            meta=None,
            **kwargs,
    ):
        super().__init__(formdata, obj, prefix, data, meta, kwargs)
        self.first_name = None

    item_name = StringField('', [validators.Length(min=1, max=10),
                                           validators.DataRequired()])

    description = TextAreaField('', [validators.Optional()])

    price = TextAreaField('', [validators.Optional()])

    allergy = TextAreaField('', [validators.Optional()])
    
    
    
    