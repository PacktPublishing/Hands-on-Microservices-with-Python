from flask import make_response, abort, request, jsonify
from passlib.hash import sha256_crypt
from . import user_api_blueprint
from models import db, User


@user_api_blueprint.route('/api/users', methods=['GET'])
def get_users():
    data = []
    for row in User.query.all():
        data.append(row.to_json())

    response = jsonify(data)

    return response


@user_api_blueprint.route('/api/user/<username>', methods=['GET'])
def get_user(username):

    data = User.query.filter_by(username=username).first()
    if data:
        response = make_response(jsonify(data.to_json()))
    else:
        response = make_response(jsonify({'message': 'Cannot find user'}), 404)

    return response


@user_api_blueprint.route('/api/user/create', methods=['POST'])
def post_register():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    username = request.form['username']

    password = sha256_crypt.encrypt((str(request.form['password'])))

    user = User()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.password = password
    user.username = username

    db.session.add(user)
    db.session.commit()

    response = jsonify({'message': 'User added', 'result': user.to_json()})

    return response
