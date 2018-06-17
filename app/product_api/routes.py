from flask import make_response, json, abort
from . import product_api_blueprint

with open('database/products.json') as f:
    data = json.load(f)


@product_api_blueprint.route('/api/products', methods=['GET'])
def products():

    response = make_response(json.dumps(data, indent=4))

    return response


@product_api_blueprint.route('/api/product/<id>', methods=['GET'])
def product(id):
    if id not in data:
        abort(404)

    response = make_response(json.dumps(data[id], indent=4))

    return response
