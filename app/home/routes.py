from flask import render_template
from . import forms
from . import home_blueprint


# Home page
@home_blueprint.route('/', methods=['GET'])
def home():

    return render_template('home/index.html')


# Login
@home_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    message = ''
    form = forms.LoginForm()

    if form.is_submitted():
        if form.validate_on_submit():
            message = 'Form is valid'
        else:
            message = 'Form is invalid'

    return render_template('login/index.html', form=form, message=message)


# Logout
@home_blueprint.route('/logout', methods=['GET'])
def logout():

    return render_template('login/index.html')


# Product page
@home_blueprint.route('/product/<id>', methods=['GET'])
def product(id):

    return render_template('product/index.html')


# Order page
@home_blueprint.route('/order', methods=['GET'])
def order():

    return render_template('order/index.html')


# Order thank you
@home_blueprint.route('/order/thank-you', methods=['GET'])
def thank_you():

    return render_template('order/thankyou.html')