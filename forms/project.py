from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectMultipleField, widgets, FieldList, FormField
from wtforms.validators import DataRequired, URL, Optional
from models.project import Tag
from models import storage


class LinkForm(FlaskForm):
    name = StringField('Name')
    url = StringField('URL', validators=[URL(), Optional()])


class ObjectiveForm(FlaskForm):
    text = StringField('Text')


class TakeawayForm(FlaskForm):
    text = StringField('Text')


class SubtitleForm(FlaskForm):
    text = StringField('Text')
    objectives = FieldList(FormField(ObjectiveForm), min_entries=30)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    demo_link = StringField('Demo Link', validators=[URL(), Optional()])
    source_link = TextAreaField('Source Link')
    image = FileField('Image')
    tags = MultiCheckboxField('Tags', coerce=str)
    links = FieldList(FormField(LinkForm), min_entries=15)
    takeaways = FieldList(FormField(TakeawayForm), min_entries=20)
    subtitles = FieldList(FormField(SubtitleForm), min_entries=10)

    def populate_tags(self, current_tags=None):
        # Populate the choices for the tags field
        self.tags.choices = [(tag.id, tag.name) for tag in storage.all(Tag).values()]
        if current_tags:
            self.tags.process_data = [tag.id for tag in current_tags]