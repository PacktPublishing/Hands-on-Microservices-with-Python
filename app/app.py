from flask import Flask
from flask_bootstrap import Bootstrap
from home import home_blueprint
from user import user_blueprint

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

app.register_blueprint(home_blueprint)
app.register_blueprint(user_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
