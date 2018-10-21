import requests


class ProductClient:

    @staticmethod
    def get_product(slug):
        response = requests.request(method="GET", url='http://product:5000/api/product/' + slug)
        product = response.json()
        return product

    @staticmethod
    def get_products():
        r = requests.get('http://product:5000/api/products')
        products = r.json()
        return products
