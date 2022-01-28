# Ashlee

from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, FileField
from wtforms.fields import StringField, SelectField, DecimalField, DateField

from application.Models.RestaurantSystem import RestaurantSystem


class CreateReviewForm(Form):
    restaurant = SelectField('Restaurant', choices=[('', '---')])
   # TODO: Make Stars a clickable star field - not used to using dropdowns
    #       and dropdowns only for 5 options max
    stars = SelectField('Stars', choices=[('', '---'), (1, '1: Very Poor'), (2, '2: Poor'), (3, '3: Average'),
                                          (4, '4: Good'), (5, '5: Excellent')])
    title = StringField('Review Title', [validators.Length(min=1, max=50), validators.DataRequired()])
    description = TextAreaField('Describe your experience (300 words maximum)',
                                [validators.Length(min=0, max=300)])
    media = FileField("Upload Media")
