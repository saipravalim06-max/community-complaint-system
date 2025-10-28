from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from flask_wtf.file import FileField, FileAllowed

class UpdateStatusForm(FlaskForm):
    status = SelectField("Status", choices=[
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    ])
    resolved_image = FileField("Resolved Image", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField("Update")
