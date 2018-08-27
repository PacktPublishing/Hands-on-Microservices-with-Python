from flask import render_template, json, session, redirect, url_for, flash, request, current_app
import requests
from flask_login import current_user, login_user
from . import forms, api
from . import frontend_blueprint

with open('database/products.json') as f:
    data = json.load(f)


def get_order():
    headers = {
        'Authorization': 'Basic ' + session['user_api_key']
    }

    response = requests.request(method="GET", url=current_app.config['API_URI'] + '/api/order', headers=headers)
    order = response.json()
    return order


def get_user():
    headers = {
        'Authorization': 'Basic ' + session['user_api_key']
    }

    response = requests.request(method="GET", url=current_app.config['API_URI'] + '/api/user', headers=headers)
    user = response.json()
    return user


def get_username(username):
    response = requests.request(method="GET", url=current_app.config['API_URI'] + '/api/user/' + username + '/exists')
    return response.status_code == 200


def get_order_from_session():
    default_order = {
        'items': {},
        'total': 0,
    }
    return session.get('order', default_order)


def get_product(slug):
    response = requests.request(method="GET", url=current_app.config['API_URI'] + '/api/product/' + slug)
    product = response.json()
    return product


def post_user_create(form):
    user = False
    payload = {
        'email': form.email.data,
        'password': form.password.data,
        'first_name': form.first_name.data,
        'last_name': form.last_name.data,
        'username': form.username.data
    }
    response = requests.request("POST", url=current_app.config['API_URI'] + '/api/user/create', data=payload)
    if response:
        user = response.json()
    return user


def post_login(form):
    api_key = False
    payload = {
        'username': form.username.data,
        'password': form.password.data,
    }
    response = requests.request("POST", url=current_app.config['API_URI'] + '/api/user/login', data=payload)
    if response:
        d = response.json()
        if d['api_key'] is not None:
            api_key = d['api_key']
    return api_key


def post_add_to_cart(product_id, qty=1):
    payload = {
        'product_id': product_id,
        'qty': qty,
    }
    headers = {
        'Authorization': 'Basic ' + session['user_api_key']
    }
    response = requests.request("POST", url=current_app.config['API_URI'] + '/api/order/add-item', data=payload, headers=headers)
    if response:
        order = response.json()

        return order


def update_order(items):

    headers = {
        'Authorization': 'Basic ' + session['user_api_key']
    }
    response = requests.request("POST", url=current_app.config['API_URI'] + '/api/order/update', data=items, headers=headers)
    if response:
        order = response.json()

        return order


# Home page
@frontend_blueprint.route('/', methods=['GET'])
def home():
    # session.clear()
    if current_user.is_authenticated:
        order = get_order()
        session['order'] = order['result']

    try:
        r = requests.get(current_app.config['API_URI'] + '/api/products')
        products = r.json()

    except requests.exceptions.ConnectionError:
        products = []

    return render_template('home/index.html', products=products)


# Login
@frontend_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('frontend.home'))

    form = forms.LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            api_key = post_login(form)
            if api_key:
                # Get the user
                session['user_api_key'] = api_key
                user = get_user()
                session['user'] = user['result']

                # Get the order
                order = get_order()
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

            # Search for existing
            user = get_username(username)
            if user:
                # Existing user found
                flash('Please try another username', 'error')
                return render_template('register/index.html', form=form)
            else:
                # Attempt to create the new user
                user = post_user_create(form)
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
    response = get_product(slug)
    product = response['result']

    form = forms.ItemForm(product_id=product['id'])

    max = 5

    if request.method == "POST":

        if session['user_api_key']:
            current_order = post_add_to_cart(product_id=product['id'], qty=1)

            stored_order = current_order['result']
        else:
            # not logged in
            stored_order = get_order_from_session()
            if product['id'] in stored_order['items']:
                qty = stored_order['items'][slug] + 1
                if qty > max:
                    flash('Cannot add any more items', 'error')
                    stored_order['items'][slug] = max
                else:
                    flash('Item added', 'success')
                    stored_order['items'][slug] += 1
            else:
                stored_order['items'].update({slug: 1})

        session['order'] = stored_order

    return render_template('product/index.html', product=product, form=form)


# ORDER PAGES


# Order summary  page
@frontend_blueprint.route('/checkout', methods=['GET', 'POST'])
def summary():

    order = get_order()

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
            id = form['product_id_' + str(foo)].data
            qty = request.form['quantity_' + str(foo)]

            payload = {
                'product_id': id,
                'qty' : qty
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