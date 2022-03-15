from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class EditCategory(FlaskForm):
    title = StringField('Title of category', validators=[DataRequired()])
    submit = SubmitField('Edit category')
