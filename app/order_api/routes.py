from flask import jsonify, request
from . import order_api_blueprint
from models import db, Order


@order_api_blueprint.route('/api/orders', methods=['GET'])
def orders():

    items = []
    for row in Order.query.all():
        items.append(row.to_json())

    response = jsonify(items)

    return response


@order_api_blueprint.route('/api/order/<id>', methods=['GET'])
def order(id):
    item = Order.query.filter_by(id=id).first()
    if item is not None:
        response = jsonify(item.to_json())
    else:
        response = jsonify({'message': 'Cannot find order'}), 404

    return response


@order_api_blueprint.route('/api/order/create', methods=['POST'])
def post_create():

    name = request.form['name']
    slug = request.form['slug']
    image = request.form['image']
    price = request.form['price']

    item = Order()
    item.name = name
    item.slug = slug
    item.image = image
    item.price = price

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'Product added', 'product': item.to_json()})

    return response
