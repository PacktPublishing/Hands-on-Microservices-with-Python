from flask import Flask, g

from flask_login import LoginManager, user_loaded_from_header
from flask_bootstrap import Bootstrap
from frontend import frontend_blueprint
from user_api import user_api_blueprint
from product_api import product_api_blueprint
from order_api import order_api_blueprint
from flask.sessions import SecureCookieSessionInterface
import models
import base64

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'frontend.login'

bootstrap = Bootstrap(app)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:test@db/order_sys',
))

models.init_app(app)
models.create_tables(app)

app.register_blueprint(frontend_blueprint)
app.register_blueprint(user_api_blueprint)
app.register_blueprint(product_api_blueprint)
app.register_blueprint(order_api_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):

    # try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    return None


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)


app.session_interface = CustomSessionInterface()


@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
