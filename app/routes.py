#from app import app
from flask import render_template
from flask import Blueprint

from . import db

routes = Blueprint('main', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/profile')
def profile():
    return render_template('profile.html')





