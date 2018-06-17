from flask import make_response, abort, request, jsonify
from . import user_api_blueprint
from models import db, Customer


@user_api_blueprint.route('/api/users', methods=['GET'])
def get_users():
    data = []
    for row in Customer.query.all():
        data.append(row.to_json())

    response = jsonify(data)

    return response


@user_api_blueprint.route('/api/user/<email>', methods=['GET'])
def get_user(email):

    data = Customer.query.filter_by(email=email).first()
    if data is None:
        abort(404)

    response = make_response(jsonify(data.to_json()))

    return response


@user_api_blueprint.route('/api/user/register', methods=['POST'])
def post_register():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email_address']

    user = Customer()
    user.email = email
    user.firstName = first_name
    user.lastName = last_name

    db.session.add(user)
    db.session.commit()

    response = jsonify({'message': 'Customer added', 'customer': user.to_json()})

    return response
