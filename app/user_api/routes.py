from flask import make_response, request, jsonify
from flask_login import current_user, login_user, logout_user
from passlib.hash import sha256_crypt
from . import user_api_blueprint
from models import db, User
from flask_login import login_required, current_user

@user_api_blueprint.route('/api/users', methods=['GET'])
def get_users():
    data = []
    for row in User.query.all():
        data.append(row.to_json())

    response = jsonify(data)

    return response


@user_api_blueprint.route('/api/user/login', methods=['POST'])
def post_login():

    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user:
        if sha256_crypt.verify(str(request.form['password']), user.password):
            user.encode_api_key()
            db.session.commit()
            login_user(user)

            return make_response(jsonify({'message': 'Logged in', 'api_key': user.api_key}))

    return make_response(jsonify({'message': 'Not logged in'}), 401)


@user_api_blueprint.route('/api/user/logout', methods=['POST'])
def post_logout():

    if current_user.is_authenticated:
        logout_user()
        return make_response(jsonify({'message': 'You are no longer logged in'}))

    return make_response(jsonify({'message': 'You are not logged in'}))


@user_api_blueprint.route('/api/user/<username>/exists', methods=['GET'])
def get_username(username):

    item = User.query.filter_by(username=username).first()
    if item is not None:
        response = jsonify({'result': True})
    else:
        response = jsonify({'message': 'Cannot find username'}), 404

    return response


@login_required
@user_api_blueprint.route('/api/user', methods=['GET'])
def get_user():

    if current_user.is_authenticated:
        return make_response(jsonify({'result': current_user.to_json()}), 404)

    return make_response(jsonify({'message': 'Not logged in'}), 401)


@user_api_blueprint.route('/api/user/create', methods=['POST'])
def post_register():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    username = request.form['username']

    password = sha256_crypt.hash((str(request.form['password'])))

    user = User()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.password = password
    user.username = username
    user.authenticated = True
    user.active = True

    db.session.add(user)
    db.session.commit()

    response = jsonify({'message': 'User added', 'result': user.to_json()})

    return response
