"""
The users Blueprint handles the user management for this application.
Specifically, this Blueprint allows for new users to register and for
users to log in and to log out of the application.
"""
from flask import Blueprint

home_blueprint = Blueprint('home', __name__, template_folder='templates')


from . import routes