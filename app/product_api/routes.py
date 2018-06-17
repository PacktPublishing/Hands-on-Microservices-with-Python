from flask import json, jsonify, request
from . import product_api_blueprint
from models import db, Product

with open('database/products.json') as f:
    data = json.load(f)


@product_api_blueprint.route('/api/products', methods=['GET'])
def products():

    items = []
    for row in Product.query.all():
        items.append(row.to_json())

    response = jsonify(items)

    return response


@product_api_blueprint.route('/api/product/<slug>', methods=['GET'])
def product(slug):
    item = Product.query.filter_by(slug=slug).first()
    if item is not None:
        response = jsonify(item.to_json())
    else:
        response = jsonify({'message': 'Cannot find product'}), 404

    return response


@product_api_blueprint.route('/api/product/create', methods=['POST'])
def post_create():

    name = request.form['name']
    slug = request.form['slug']
    image = request.form['image']
    price = request.form['price']

    item = Product()
    item.name = name
    item.slug = slug
    item.image = image
    item.price = price

    db.session.add(item)
    db.session.commit()

    response = jsonify({'message': 'Product added', 'product': item.to_json()})

    return response
