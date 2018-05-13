from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'thisneedstobechanged'


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/', methods=['GET', 'POST'])
def login():

    message = ''
    form = LoginForm()

    if form.is_submitted():
        if form.validate_on_submit():
            message = 'Form is valid'
        else:
            message = 'Form is invalid'

    return render_template('login/index.html', form=form, message=message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
