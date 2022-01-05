# xu yong lin
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RestaurantCertification(FlaskForm):
    hygiene_cert = FileField('hygieneInput',
                             validators=[FileRequired(), FileAllowed(['pdf'], "wrong format!")])
    halal_cert = FileField('Halal',
                           validators=[FileRequired(), FileAllowed(['pdf'], 'Wrong format!')])
    vegetarian_cert = FileField('Vegetarian', validators=[FileRequired(),
                                                          FileAllowed(['pdf'])])
    vegan_cert = FileField('Vegan',
                           validators=[FileRequired(), FileAllowed(['pdf'])])
    submit = SubmitField('Submit')
