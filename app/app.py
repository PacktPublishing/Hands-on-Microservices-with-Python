from flask import Blueprint, Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from frontend import frontend_blueprint

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'main.login'

bootstrap = Bootstrap(app)


app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    PRODUCT_SERVICE= 'http://192.168.99.100:8081'
))

app.register_blueprint(frontend_blueprint)

app.run(debug=True, host='0.0.0.0')

