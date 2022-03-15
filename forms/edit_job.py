from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from wtforms import SubmitField, BooleanField, StringField, IntegerField, DateField, SelectMultipleField, SelectField


class EditJob(FlaskForm):
    team_leader = SelectField('Team leader', validators=[DataRequired()], coerce=int,
                              choices=[(int(i.split()[0]), f'{i.split()[1]} {i.split()[2]}') for i in
                                       open("users.txt").read().split('\n')[:-1]])
    job = StringField('Title of activity', validators=[DataRequired()])
    work_size = IntegerField('Duration (in hours)', validators=[DataRequired(), NumberRange(min=1)])
    collaborators = StringField('List of collaborators id', validators=[DataRequired()])
    categories = SelectMultipleField('Hazard category', validators=[DataRequired()], coerce=int,
                                     choices=[(int(i.split()[0]), i.split()[1]) for i in
                                              open("categories.txt").read().split('\n')[:-1]])
    start_date = DateField('Start date')
    end_date = DateField('End date')
    is_finished = BooleanField('Is finished')
    submit = SubmitField('Edit job')
