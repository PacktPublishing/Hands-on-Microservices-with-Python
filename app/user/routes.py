from flask import make_response, json, abort
from . import user_blueprint

with open('database/users.json') as f:
    data = json.load(f)


@user_blueprint.route('/api/users', methods=['GET'])
def users():

    response = make_response(json.dumps(data, indent=4))

    return response


@user_blueprint.route('/api/user/<username>', methods=['GET'])
def user(username):
    if username not in data:
        abort(404)

    response = make_response(json.dumps(data[username], indent=4))

    return response


@user_blueprint.route('/api/user/register', methods=['POST'])
def register(username):
    if username not in data:
        abort(404)

    response = make_response(json.dumps(data[username], indent=4))

    return response


@user_blueprint.route('/api/user/login', methods=['POST'])
def login(username):
    if username not in data:
        abort(404)

    response = make_response(json.dumps(data[username], indent=4))

    return response
