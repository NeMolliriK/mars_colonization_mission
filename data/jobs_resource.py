from flask_restful import reqparse, abort, Resource
from . import db_session
from .jobs import Job
from flask import jsonify
from datetime import date


def abort_if_user_not_found(job_id):
    if not db_session.create_session().query(Job).get(job_id):
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_user_not_found(job_id)
        return jsonify({'job': db_session.create_session().query(Job).get(job_id).to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))})

    def delete(self, job_id):
        abort_if_user_not_found(job_id)
        db_sess = db_session.create_session()
        db_sess.delete(db_sess.query(Job).get(job_id))
        db_sess.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        return jsonify({'jobs': [job.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
            for job in db_session.create_session().query(Job).all()]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        job = Job(team_leader=args['team_leader'], job=args['job'], work_size=args['work_size'],
                  collaborators=args['collaborators'], start_date=args.get('start_date', date(1, 1, 1)),
                  end_date=args.get('end_date', date(1, 1, 1)), is_finished=args['is_finished'])
        db_sess.add(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('start_date', type=date)
parser.add_argument('end_date', type=date)
parser.add_argument('is_finished', required=True, type=bool)
