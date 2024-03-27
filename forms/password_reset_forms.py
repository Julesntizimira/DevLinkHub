from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectMultipleField, widgets, FieldList, FormField, EmailField
from wtforms.validators import DataRequired, URL, Optional
from models.project import Tag
from models import storage


class ForgotPasswordForm(FlaskForm):
    title = EmailField('Email', validators=[DataRequired()])