from flask_restful import reqparse, abort, Resource
from . import db_session
from .users import User
from flask import jsonify
from datetime import datetime


def abort_if_user_not_found(user_id):
    if not db_session.create_session().query(User).get(user_id):
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        return jsonify({'user': db_session.create_session().query(User).get(user_id).to_dict(only=(
            'id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password',
            'modified_date', "city_from"))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        db_sess.delete(db_sess.query(User).get(user_id))
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        return jsonify({'users': [user.to_dict(only=(
            'id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password',
            'modified_date', 'city_from')) for user in db_session.create_session().query(User).all()]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = User(surname=args['surname'], name=args['name'], age=args['age'], position=args['position'],
                    speciality=args['speciality'], address=args['address'], email=args['email'],
                    city_from=args['city_from'], modified_date=args.get('modified_date', datetime.now()))
        user.set_password(args['password'])
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('modified_date', type=datetime)
parser.add_argument('password', required=True)
parser.add_argument('city_from', required=True)
