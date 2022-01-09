# xu yong lin
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class DocumentUploadForm(FlaskForm):
    hygiene_doc = FileField('hygieneDocument', validators=[FileRequired()])
    submit = SubmitField('Submit')

# # for file validation
# class RestaurantCertification(FlaskForm):
#     hygiene_cert = FileField('hygieneInput',
#                              validators=[FileRequired()])
#     halal_cert = FileField('Halal',
#                            validators=[FileRequired()])
#     vegetarian_cert = FileField('Vegetarian', validators=[FileRequired(),
#                                                           ])
#     vegan_cert = FileField('Vegan',
#                            validators=[FileRequired()])
#     submit = SubmitField('Submit')
