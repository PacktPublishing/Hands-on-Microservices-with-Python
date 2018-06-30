from flask import render_template, json, session, redirect, url_for, flash, request
import requests
from . import forms, api
from . import frontend_blueprint

with open('database/products.json') as f:
    data = json.load(f)


def get_order():
    order = {}
    order_id = session.get('order_id')

    if order_id:
        response = requests.get('http://192.168.99.102/api/order/' + order_id)
        order = response.json()
    return order


def get_user_by_username(username):
    user = False
    response = requests.get('http://192.168.99.102/api/user/' + username)
    if response:
        user = response.json()
    return user


def post_user_create(form):
    user = False
    payload = {
            'email': form.email.data,
            'password': form.password.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'username': form.username.data
    }
    url = 'http://192.168.99.102/api/user/create'
    response = requests.request("POST", url=url, data=payload)
    if response:
        user = response.json()
    return user


# Home page
@frontend_blueprint.route('/', methods=['GET'])
def home():

    order = get_order()

    try:
        r = requests.get('http://192.168.99.102/api/products')
        products = r.json()

    except requests.exceptions.ConnectionError:
        products = []

    return render_template('home/index.html', products=products, order=order)


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


# Register new customer
@frontend_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    form = forms.RegisterForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data

            # Search for existing
            user = get_user_by_username(username)
            if user:
                # Existing user found
                flash('Please try another username', 'error')
                return render_template('register/index.html', form=form)
            else:
                # Attempt to create the new user
                user = post_user_create(form)
                if user:
                    # Store user ID in session and redirect
                    flash('Thanks for registering!', 'success')
                    session['username'] = username
                    return redirect(url_for('frontend.home'))

        else:
            flash('Errors found', 'error')

    return render_template('register/index.html', form=form)


# Logout
@frontend_blueprint.route('/logout', methods=['GET'])
def logout():

    return render_template('login/index.html')


# Product page
@frontend_blueprint.route('/product/<slug>', methods=['GET'])
def product(slug):

    order = get_order()

    item = api.get_request('http://192.168.99.102/api/product/' + slug)

    # try:
    #     r = requests.get('http://192.168.99.102/api/product/' + slug)
    #     r.raise_for_status()
    #     item = r.json()
    # except requests.exceptions.ConnectionError:
    #     abort(404)

    return render_template('product/index.html', product=item, order=order)


# ORDER PAGES

# Order add item page
@frontend_blueprint.route('/order/add-item', methods=['POST'])
def add_item():

    user = get_user()
    if user is False:
        return redirect(url_for('frontend.login'))

    """
    - Create the order if needed
    - Add item to order
    - Redirect to order summary
    """

    return render_template('order/index.html')


# Order summary  page
@frontend_blueprint.route('/order/summary', methods=['GET'])
def summary():
    """ Display a list of order items for current user"""

    return render_template('order/summary.html')


# Order thank you
@frontend_blueprint.route('/order/thank-you', methods=['GET'])
def thank_you():

    return render_template('order/thankyou.html')