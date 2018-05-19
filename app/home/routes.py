from flask import render_template
from . import forms
from . import home_blueprint


@home_blueprint.route('/', methods=['GET', 'POST'])
def login():

    message = ''
    form = forms.LoginForm()

    if form.is_submitted():
        if form.validate_on_submit():
            message = 'Form is valid'
        else:
            message = 'Form is invalid'

    return render_template('login/index.html', form=form, message=message)
