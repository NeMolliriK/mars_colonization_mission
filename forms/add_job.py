from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from wtforms import SubmitField, BooleanField, StringField, IntegerField, DateField
from datetime import date


class AddJob(FlaskForm):
    team_leader = IntegerField('Team leader id', validators=[DataRequired(), NumberRange(min=1)])
    job = StringField('Title of activity', validators=[DataRequired()])
    work_size = IntegerField('Duration (in hours)', validators=[DataRequired(), NumberRange(min=1)])
    collaborators = StringField('List of collaborators id', validators=[DataRequired()])
    categories = StringField('List of hazard categoryies id', validators=[DataRequired()])
    start_date = DateField('Start date', default=date(1, 1, 1))
    end_date = DateField('End date', default=date(1, 1, 1))
    is_finished = BooleanField('Is finished')
    submit = SubmitField('Add job')
