from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RestaurantCertification(Form):
    hygiene_cert = FileField('Document', validators=[FileRequired(), FileAllowed(['pdf']), 'PDF Document only!'])
    halal_cert = FileField('Document', validators=[FileRequired(), FileAllowed(['pdf']), 'PDF Document only!'])
    vegetarian_cert = FileField('Document', validators=[FileRequired(), FileAllowed(['pdf']), 'PDF Document only!'])
    vegan_cert = FileField('Document', validators=[FileRequired(), FileAllowed(['pdf']), 'PDF Document only!'])

