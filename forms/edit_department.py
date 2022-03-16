from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, EmailField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class EditDepartment(FlaskForm):
    title = StringField('Title of department', validators=[DataRequired()])
    chief = IntegerField('Chief id', validators=[DataRequired(), NumberRange(min=1)])
    members = StringField('Members id', validators=[DataRequired()])
    email = EmailField('Department Email', validators=[DataRequired()])
    submit = SubmitField('Edit Department')
