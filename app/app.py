from flask import Flask

from flask_bootstrap import Bootstrap
from frontend import frontend_blueprint
from user_api import user_api_blueprint
from product_api import product_api_blueprint
from models import db

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:test@db/order',
    SQLALCHEMY_TRACK_MODIFICATIONS='False'
))
db.init_app(app)

app.register_blueprint(frontend_blueprint)
app.register_blueprint(user_api_blueprint)
app.register_blueprint(product_api_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
