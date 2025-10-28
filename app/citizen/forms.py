from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, widgets, SelectMultipleField,MultipleFileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed,FileRequired

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ComplaintForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    address = TextAreaField("Address", validators=[DataRequired()])
    departments = SelectMultipleField("Departments", coerce=int, validators=[DataRequired()])
    images = FileField("Upload Images (Optional)")
    submit = SubmitField("Submit Complaint")


