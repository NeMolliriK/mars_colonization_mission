import flask
from flask import jsonify, request, render_template
from . import db_session
from .users import User
from requests import get
from datetime import datetime

blueprint = flask.Blueprint('users_api', __name__, template_folder='templates')


def map_size(c):
    c = c["boundedBy"]["Envelope"]
    q, w, a, s = list(map(float, c["lowerCorner"].split())) + list(map(float, c["upperCorner"].split()))
    return f'{abs(q - a)},{abs(w - s)}'


@blueprint.route('/api/users')
def get_users():
    return jsonify({'users': [user.to_dict(only=(
        'id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password',
        'modified_date', 'city_from'))
        for user in db_session.create_session().query(User).all()]})


@blueprint.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = db_session.create_session().query(User).get(user_id)
    if user:
        return jsonify({'user': user.to_dict(only=(
            'id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password',
            'modified_date', 'city_from'))})
    return jsonify({'error': 'Not found'})


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password', "city_from"]):
        return jsonify({'error': 'Bad request'})
    elif "id" in request.json.keys() and request.json["id"] in [user.id for user in db_sess.query(User)]:
        return jsonify({'error': 'Id already exists'})
    user = User(surname=request.json['surname'], name=request.json['name'], age=request.json['age'],
                position=request.json['position'], speciality=request.json['speciality'],
                address=request.json['address'], email=request.json['email'], city_from=request.json['city_from'],
                modified_date=request.json.get('modified_date', datetime.now()))
    if "id" in request.json.keys():
        user.id = request.json['id']
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if user:
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})
    return jsonify({'error': 'Not found'})


@blueprint.route('/api/users/<int:user_id>', methods=['GET', 'PUT'])
def edit_user(user_id):
    if request.json:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        if user:
            user.name = request.json.get('name', user.name)
            user.surname = request.json.get('surname', user.surname)
            user.age = request.json.get('age', user.age)
            user.position = request.json.get('position', user.position)
            user.speciality = request.json.get('speciality', user.speciality)
            user.address = request.json.get('address', user.address)
            user.email = request.json.get('email', user.email)
            user.city_from = request.json.get('city_from', user.city_from)
            user.modified_date = request.json.get('modified_date', user.modified_date)
            user.surname = request.json.get('surname', user.surname)
            if "password" in request.json.keys():
                user.set_password(request.json["password"])
            db_sess.commit()
            return jsonify({'success': 'OK'})
        return jsonify({'error': 'Not found'})
    return jsonify({'error': 'Empty request'})


@blueprint.route('/users_show/<int:user_id>')
def users_show(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    response = get(f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode="
                   f"{user.city_from}&format=json").json()["response"]["GeoObjectCollection"]["featureMember"][0][
        "GeoObject"]
    with open("static/img/img.png", "wb") as img:
        img.write(get(f'https://static-maps.yandex.ru/1.x/?ll={response["Point"]["pos"].replace(" ", ",")}&l=sat,skl&sp'
                      f'n={map_size(response)}').content)
    return render_template("users_show.html", name=f'{user.surname} {user.name}', city=user.city_from)
