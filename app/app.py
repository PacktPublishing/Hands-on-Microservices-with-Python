from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from frontend import frontend_blueprint
from user_api import user_api_blueprint
from product_api import product_api_blueprint

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:test@db/order'
))
#pip install mysql-connector flask-sqlalchemy mysqlclient
#mysql+mysqlconnector:
#SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:test@db/order'
#SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:test@db/order'
#SQLALCHEMY_DATABASE_URI='sqlite:///order1.sqlite3'

app.register_blueprint(frontend_blueprint)
app.register_blueprint(user_api_blueprint)
app.register_blueprint(product_api_blueprint)

db = SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(120), unique=False, nullable=True)
    lastName = db.Column(db.String(120), unique=False, nullable=True)
    orders = db.relationship('Order', backref='order')
    dateAdded = db.Column(db.DateTime, default=datetime.utcnow)
    dateUpdated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=True)
    dateAdded = db.Column(db.DateTime, default=datetime.utcnow)
    dateUpdated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    image = db.Column(db.String(120), unique=False, nullable=True)
    items = db.relationship('OrderItem', backref='orderItem')
    dateAdded = db.Column(db.DateTime, default=datetime.utcnow)
    dateUpdated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    dateAdded = db.Column(db.DateTime, default=datetime.utcnow)
    dateUpdated = db.Column(db.DateTime, onupdate=datetime.utcnow)


db.create_all()

# user = Customer()
# user.email = 'test1@test.com'
# user.firstName = 'Test'
# user.lastName = 'Test'
#
# db.session.add(user)
#
# db.session.commit()

# Customer.query.all()
#
# foo = Customer.query.filter_by(email='test1@test.com').first()
#
# print(foo.id)
# print(foo.email)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
