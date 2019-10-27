#from app import app
from flask import render_template
from flask import Blueprint
from flask_login import login_required, current_user

from . import db

routes = Blueprint('main', __name__)

@routes.route('/')
def index():
    return render_template('index.html', list = )

@routes.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)





