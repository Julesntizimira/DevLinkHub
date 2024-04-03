'''create note form'''
from flask_wtf import FlaskForm
from wtforms import TextAreaField


class NoteForm(FlaskForm):
    text = TextAreaField('Note')