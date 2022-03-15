from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, IntegerField, DateField
from wtforms.validators import DataRequired


class EditJob(FlaskForm):
    team_leader = IntegerField('Team leader', validators=[DataRequired()])
    job = StringField('Title of activity', validators=[DataRequired()])
    work_size = IntegerField('Duration', validators=[DataRequired()])
    collaborators = StringField('List of collaborators', validators=[DataRequired()])
    start_date = DateField('Start date')
    end_date = DateField('End date')
    is_finished = BooleanField('Is finished')
    submit = SubmitField('Edit Job')
