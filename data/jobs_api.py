import flask
from flask import jsonify, request
from . import db_session
from .jobs import Job

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    jobs = db_session.create_session().query(Job).all()
    return jsonify({'jobs': [job.to_dict(
        only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished')) for
        job in jobs]})


@blueprint.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    job = db_session.create_session().query(Job).get(job_id)
    if job:
        return jsonify({'job': job.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))})
    return jsonify({'error': 'Not found'})


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = Job(team_leader=request.json['team_leader'], job=request.json['job'], work_size=request.json['work_size'],
              collaborators=request.json['collaborators'], is_finished=request.json['is_finished'])
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).get(job_id)
    if job:
        db_sess.delete(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})
    return jsonify({'error': 'Not found'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET', 'PUT'])
def edit_job(job_id):
    if request.json:
        db_sess = db_session.create_session()
        job = db_sess.query(Job).get(job_id)
        if job:
            job.team_leader = request.json.get('team_leader', job.team_leader)
            job.job = request.json.get('job', job.job)
            job.work_size = request.json.get('work_size', job.work_size)
            job.collaborators = request.json.get('collaborators', job.collaborators)
            job.start_date = request.json.get('start_date', job.start_date)
            job.end_date = request.json.get('end_date', job.end_date)
            job.is_finished = request.json.get('is_finished', job.is_finished)
            db_sess.commit()
            return jsonify({'success': 'OK'})
        return jsonify({'error': 'Not found'})
    return jsonify({'error': 'Empty request'})
