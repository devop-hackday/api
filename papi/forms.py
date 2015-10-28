from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class UploadForm(Form):
    filen = StringField('file', validators=[DataRequired()])
