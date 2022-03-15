from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, EmailField, SelectField
from wtforms.validators import DataRequired


class EditDepartment(FlaskForm):
    chief = SelectField('Chief', validators=[DataRequired()], coerce=int,
                        choices=[(int(i.split()[0]), f'{i.split()[1]} {i.split()[2]}') for i in
                                 open("users.txt").read().split('\n')[:-1]])
    members = StringField('Members id', validators=[DataRequired()])
    email = EmailField('Department Email', validators=[DataRequired()])
    submit = SubmitField('Edit Department')
