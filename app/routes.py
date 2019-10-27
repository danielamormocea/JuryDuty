#from app import app
from flask import render_template, request, redirect, url_for, flash
from flask import Blueprint
from flask_login import login_required, current_user
from .models import User, Contestant
from . import db

routes = Blueprint('main', __name__)

contest_name = ""
contest_rounds = 0
contest_series = 0
i = 0

@routes.route('/')
def index():
    contestants = Contestant.query.all()
    # contestans = {<Contestant 1>, <Contestant 12>, <Contestant 2> ....}
    # contestant[0] -> Contestant 1
    # contestant[0].age, contestant[0].name ... etc
    # ex: for contestant in contestants:
    #       print contestant.age
    return render_template('index.html', contestans = contestants)


@routes.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)


@routes.route ('/organize', methods=['GET'])
def organize():
    return render_template('organize.html')

@routes.route ('/organize', methods=['POST'])
def organize_post():
    contest_name = request.form.get('contest_name')
    contest_rounds = request.form.get('round_no')
    contest_series = request.form.get('series_no')
    return redirect(url_for('main.add_contestant'))

@routes.route('/add_contestant' , methods=['GET'])
def add_contestant():
    return render_template('add_contestant.html')


@routes.route('/add_contestant' , methods=['POST'])
def add_contestant_post():
    global i
    contestant_name = request.form.get('name_contestant')
    age = request.form.get('age')
    description = request.form.get('description')
    i += 1
    new_contestant = Contestant( id = i, name = contestant_name, age = age, description = description, round_no = 0, series_no = 0, grade = 0)

    db.session.add(new_contestant)
    db.session.commit()

    return redirect(url_for('main.add_contestant_post'))


    







