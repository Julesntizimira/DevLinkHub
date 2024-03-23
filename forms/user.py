from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, EmailField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, URL, Optional



class UserForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = StringField('Enter Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    profile_image = FileField('Profile Image')


class ProfileForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    location = StringField('Location')
    bio = TextAreaField('Bio')
    headline = StringField('Headline')
    social_github = StringField('gitHub link', validators=[URL(), Optional()])
    social_linkdin = StringField('LinkdIn', validators=[URL(), Optional()])
    social_youtube = StringField('Youtube link', validators=[URL(), Optional()])
    social_twitter = StringField('twitter link', validators=[URL(), Optional()])
    profile_image = FileField('Profile Image')


class SkillForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")