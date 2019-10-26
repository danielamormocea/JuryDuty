#from app import app
from flask import render_template
from flask import Blueprint

from . import db

routes = Blueprint('main', __name__)

@routes.route('/')
def index():
    return 'Index'

@routes.route('/profile')
def profile():
    return 'Profile'



