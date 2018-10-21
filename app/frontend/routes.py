from flask import render_template, session, redirect, url_for, flash, request
import requests
from flask_login import current_user
from . import forms
from . import frontend_blueprint
from .api.UserClient import UserClient
from .api.OrderClient import OrderClient
from .api.ProductClient import ProductClient


# Home page
@frontend_blueprint.route('/', methods=['GET'])
def home():
    # session.clear()
    if current_user.is_authenticated:
        # order = order
        session['order'] = OrderClient.get_order_from_session()

    try:
        products = ProductClient.get_products()
    except requests.exceptions.ConnectionError:
        products = {
            'results': []
        }

    return render_template('home/index.html', products=products)


# Login
@frontend_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.home'))

    form = forms.LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            api_key = UserClient.post_login(form)
            if api_key:
                # Get the user
                session['user_api_key'] = api_key
                user = UserClient.get_user()
                session['user'] = user['result']

                # Get the order
                order = OrderClient.get_order()
                if order.get('result', False):
                    session['order'] = order['result']

                # Existing user found
                flash('Welcome back, ' + user['result']['username'], 'success')
                return redirect(url_for('frontend.home'))
            else:
                flash('Cannot login', 'error')
        else:
            flash('Errors found', 'error')
    return render_template('login/index.html', form=form)


# Register new customer
@frontend_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    form = forms.RegisterForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data

            # Search for existing user
            user = UserClient.does_exist(username)
            if user:
                # Existing user found
                flash('Please try another username', 'error')
                return render_template('register/index.html', form=form)
            else:
                # Attempt to create the new user
                user = UserClient.post_user_create(form)
                if user:
                    # Store user ID in session and redirect
                    flash('Thanks for registering, please login', 'success')
                    return redirect(url_for('frontend.login'))

        else:
            flash('Errors found', 'error')

    return render_template('register/index.html', form=form)


# Logout
@frontend_blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('frontend.home'))


# Product page
@frontend_blueprint.route('/product/<slug>', methods=['GET', 'POST'])
def product(slug):

    # Get the product
    response = ProductClient.get_product(slug)
    item = response['result']

    form = forms.ItemForm(product_id=item['id'])

    if request.method == "POST":

        if 'user' not in session:
            flash('Please login', 'error')
            return redirect(url_for('frontend.login'))

        order = OrderClient.post_add_to_cart(product_id=item['id'], qty=1)
        session['order'] = order['result']
        flash('Order has been updated', 'success')

    return render_template('product/index.html', product=item, form=form)


# ORDER PAGES


# Order summary  page
@frontend_blueprint.route('/checkout', methods=['GET'])
def summary():

    if 'user' not in session:
        flash('Please login', 'error')
        return redirect(url_for('frontend.login'))

    if 'order' not in session:
        flash('No order found', 'error')
        return redirect(url_for('frontend.home'))

    order = OrderClient.get_order()

    if len(order['result']['items']) == 0:
        flash('No order found', 'error')
        return redirect(url_for('frontend.home'))

    OrderClient.post_checkout()

    return redirect(url_for('frontend.thank_you'))


# Order thank you
@frontend_blueprint.route('/order/thank-you', methods=['GET'])
def thank_you():

    if 'user' not in session:
        flash('Please login', 'error')
        return redirect(url_for('frontend.login'))

    if 'order' not in session:
        flash('No order found', 'error')
        return redirect(url_for('frontend.home'))

    session.pop('order', None)
    flash('Thank you for your order', 'success')

    return render_template('order/thankyou.html')
