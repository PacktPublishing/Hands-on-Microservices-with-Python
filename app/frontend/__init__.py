from flask import Blueprint

frontend_blueprint = Blueprint('frontend', __name__, template_folder='templates')

from . import routes
