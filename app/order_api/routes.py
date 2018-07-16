from flask import jsonify, request
from . import order_api_blueprint
from models import db, Order, OrderItem
from app import load_user_from_request
from flask_login import login_required, current_user

@order_api_blueprint.route('/api/orders', methods=['GET'])
def orders():

    items = []
    for row in Order.query.all():
        items.append(row.to_json())

    response = jsonify(items)

    return response

@login_required
@order_api_blueprint.route('/api/order/add-item', methods=['POST'])
def order_add_item():

    if not current_user.is_authenticated:
        return jsonify({'message': 'Access Denied'}), 401

    p_id = int(request.form['product_id'])
    qty = int(request.form['qty'])
    u_id = int(current_user.id)

    # Find open order
    known_order = Order.query.filter_by(user_id=u_id, is_open=1).first()

    if known_order is None:
        # Create the order
        known_order = Order()
        known_order.is_open = True
        known_order.user_id = u_id

        order_item = OrderItem()
        order_item.product_id = p_id
        order_item.quantity = qty
        known_order.items.append(order_item)

    else:
        found = False
        # Check if we already have an order item with that product
        for item in known_order.items:

            if item.product.id == p_id:
                found = True
                item.quantity += qty

        if found is False:
            order_item = OrderItem()
            order_item.product_id = p_id
            known_order.items.append(order_item)

    db.session.add(known_order)
    db.session.commit()

    response = jsonify({'result': known_order.to_json()})

    return response


@login_required
@order_api_blueprint.route('/api/order/update', methods=['POST'])
def order_update():

    if not current_user.is_authenticated:
        return jsonify({'message': 'Access Denied'}), 401

    items = request.form['items']

    u_id = int(current_user.id)

    # Find open order
    known_order = Order.query.filter_by(user_id=u_id, is_open=1).first()

    if known_order is None:
        # Create the order
        known_order = Order()
        known_order.create()

    # Delete any exiting order items
    known_order.items = []

    for item in items:
        order_item = OrderItem(item.product.id, item.quantity)
        known_order.items.append(order_item)

    db.session.add(known_order)
    db.session.commit()

    response = jsonify({'result': known_order.to_json()})

    return response

@login_required
@order_api_blueprint.route('/api/order', methods=['GET'])
def order():
    if not current_user.is_authenticated:
        return jsonify({'message': 'Access Denied'}), 401

    open_order = Order.query.filter_by(user_id=current_user.id, is_open=1).first()

    if open_order is None:
        response = jsonify({'message': 'No order found'})
    else:
        response = jsonify({'result': open_order.to_json()})

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
