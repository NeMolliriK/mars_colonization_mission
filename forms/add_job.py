from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, IntegerField, DateField
from wtforms.validators import DataRequired
from datetime import date


class AddJob(FlaskForm):
    team_leader = IntegerField('Team leader', validators=[DataRequired()])
    job = StringField('Title of activity', validators=[DataRequired()])
    work_size = IntegerField('Duration', validators=[DataRequired()])
    collaborators = StringField('List of collaborators', validators=[DataRequired()])
    start_date = DateField('Start date', default=date(1, 1, 1))
    end_date = DateField('End date', default=date(1, 1, 1))
    is_finished = BooleanField('Is finished')
    submit = SubmitField('Add job')
