from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired


class EditJob(FlaskForm):
    team_leader = SelectField('Team leader', validators=[DataRequired()], coerce=int,
                              choices=[(int(i.split()[0]), f'{i.split()[1]} {i.split()[2]}') for i in
                                       open("users.txt").read().split('\n')[:-1]])
    job = StringField('Title of activity', validators=[DataRequired()])
    work_size = IntegerField('Duration (in hours)', validators=[DataRequired()])
    collaborators = StringField('List of collaborators id', validators=[DataRequired()])
    start_date = DateField('Start date')
    end_date = DateField('End date')
    is_finished = BooleanField('Is finished')
    submit = SubmitField('Edit Job')
