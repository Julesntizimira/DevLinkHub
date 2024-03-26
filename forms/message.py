from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField


class MessageForm(FlaskForm):
    subject = StringField('Subject')
    message = TextAreaField('Message')
