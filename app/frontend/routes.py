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

        if not current_user.is_authenticated:
            flash('Please login')
            return redirect(url_for('frontend.login'))

        OrderClient.post_add_to_cart(product_id=item['id'], qty=1)

    return render_template('product/index.html', product=item, form=form)


# ORDER PAGES


# Order summary  page
@frontend_blueprint.route('/checkout', methods=['GET', 'POST'])
def summary():

    if not current_user.is_authenticated:
        flash('No order found')
        return redirect(url_for('frontend.home'))

    order = OrderClient.get_order()

    class SummaryForm(forms.FlaskForm):
        pass
        submit = forms.SubmitField('Update')

    index = 0
    for row in order['result']['items']:
        index += 1
        product_id = forms.HiddenField(validators=[forms.DataRequired()], default=row)
        choices = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
        quantity = forms.SelectField(choices=choices, default=row['quantity'])

        setattr(SummaryForm, 'product_id_' + str(index), product_id)
        setattr(SummaryForm, 'quantity_' + str(index), quantity)

    form = SummaryForm()
    items = []
    if request.method == "POST":
        foo = 0
        for row in list(order['result']['items']):
            foo += 1

            payload = {
                'product_id': form['product_id_' + str(foo)].data,
                'qty': request.form['quantity_' + str(foo)]
            }
            items.append(payload)

        # order = update_order(items)

        flash('Order has been updated', 'success')
        # session['order'] = order['result']

    return render_template('order/summary.html', order=order, form=form, items=items)


# Order thank you
@frontend_blueprint.route('/order/thank-you', methods=['GET'])
def thank_you():

    return render_template('order/thankyou.html')
