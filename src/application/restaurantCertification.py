# xu yong lin
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class DocumentUploadForm(FlaskForm):
    hygiene_doc = FileField('hygieneDocument', validators=[FileRequired()])
    submit = SubmitField('Submit')

