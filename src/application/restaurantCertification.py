from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RestaurantCertification(Form):
    hygiene_cert = FileField('Hygiene Certification', validators=[FileRequired(), FileAllowed(['pdf'])])
    halal_cert = FileField('Halal', validators=[FileRequired(), FileAllowed(['pdf'])])
    vegetarian_cert = FileField('Vegetarian', validators=[FileRequired(), FileAllowed(['pdf'])])
    vegan_cert = FileField('Vegan', validators=[FileRequired(), FileAllowed(['pdf'])])
