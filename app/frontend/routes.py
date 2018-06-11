from flask import render_template, json
from . import forms
from . import frontend_blueprint

with open('database/products.json') as f:
    data = json.load(f)


# Home page
@frontend_blueprint.route('/', methods=['GET'])
def home():
    # Make API request to /api/products
    # r = requests.get('http://192.168.99.100/api/products')
    # data = r.json

    return render_template('home/index.html', products=data)


# Login
@frontend_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    message = ''
    form = forms.LoginForm()

    if form.is_submitted():
        if form.validate_on_submit():
            message = 'Form is valid'
        else:
            message = 'Form is invalid'

    return render_template('login/index.html', form=form, message=message)


# Register
@frontend_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    message = ''
    form = forms.RegisterForm()

    if form.is_submitted():
        if form.validate_on_submit():
            message = 'Form is valid'
        else:
            message = 'Form is invalid'

    return render_template('register/index.html', form=form, message=message)


# Logout
@frontend_blueprint.route('/logout', methods=['GET'])
def logout():

    return render_template('login/index.html')


# Product page
@frontend_blueprint.route('/product/<id>', methods=['GET'])
def product(id):
    data = []
    # Make API request to /api/products
    # r = requests.get('http://192.168.99.100/api/product/id')
    # data = r.json
    return render_template('product/index.html', product=data)


# Order page
@frontend_blueprint.route('/order', methods=['GET'])
def order():

    return render_template('order/index.html')


# Order thank you
@frontend_blueprint.route('/order/thank-you', methods=['GET'])
def thank_you():

    return render_template('order/thankyou.html')