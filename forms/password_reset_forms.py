from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL, Optional, EqualTo
from models.project import Tag
from models import storage


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])


class EnterResetTokenForm(FlaskForm):
    token = StringField('Enter Reset Token', validators=[DataRequired()])

class NewPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirmation_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
