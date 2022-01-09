# xu yong lin
from flask_wtf import FlaskForm
from wtforms import validators
from flask_wtf.file import FileField


class DocumentUploadForm(FlaskForm):
    rest_name = FileField('Hygiene Document', [validators.DataRequired()])

