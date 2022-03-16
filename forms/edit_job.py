from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange
from wtforms import SubmitField, BooleanField, StringField, IntegerField, DateField


class EditJob(FlaskForm):
    team_leader = IntegerField('Team leader id', validators=[DataRequired(), NumberRange(min=1)])
    job = StringField('Title of activity', validators=[DataRequired()])
    work_size = IntegerField('Duration (in hours)', validators=[DataRequired(), NumberRange(min=1)])
    collaborators = StringField('List of collaborators id', validators=[DataRequired()])
    categories = StringField('List of hazard categoryies id', validators=[DataRequired()])
    start_date = DateField('Start date')
    end_date = DateField('End date')
    is_finished = BooleanField('Is finished')
    submit = SubmitField('Edit job')
