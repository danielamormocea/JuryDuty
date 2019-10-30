#from app import app
from flask import render_template, request, redirect, url_for, flash
from flask import Blueprint
from flask_login import login_required, current_user
from .models import User, Contestant
from . import db
import uuid

routes = Blueprint('main', __name__)

contest_name = ""
contest_rounds = 1
contest_series = 3
categories = ["Plating", "Taste", "Smell", "Colour"]

@routes.route('/')
def index():
    contestants = Contestant.query.all()
    # contestans = {<Contestant 1>, <Contestant 12>, <Contestant 2> ....}
    # contestant[0] -> Contestant 1
    # contestant[0].age, contestant[0].name ... etc
    # ex: for contestant in contestants:
    #       print contestant.age
    print(contestants)
    return render_template('index.html', contestants = contestants)


@routes.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)


@routes.route ('/organize', methods=['GET'])
def organize():
    return render_template('organize.html', categories = categories)

@routes.route ('/organize', methods=['POST'])
def organize_post():
    global contest_name 
    contest_name = request.form.get('contest_name')
    global contest_rounds 
    contest_rounds = int(request.form.get('round_no'))
    global contest_series
    contest_series = int(request.form.get('series_no'))
    print(contest_series)
    return redirect(url_for('main.add_contestant'))

@routes.route('/add_contestant' , methods=['GET'])
def add_contestant():
    return render_template('add_contestant.html')


@routes.route('/add_contestant' , methods=[ 'POST'])
def add_contestant_post():
    global i
    if request.form.get('name_contestant') != None:
        contestant_name = request.form.get('name_contestant')
        age = request.form.get('age')
        description = request.form.get('description')
        i = uuid.uuid1()
        new_contestant = Contestant( id = i, name = contestant_name, age = age, description = description, round_no = 0, series_no = 0, grade = 0)

        db.session.add(new_contestant)
        db.session.commit()

    if request.form.get('finish') == "Finish":
        print(contest_series)
        contestants = Contestant.query.all()
        for contestant in contestants:
            contestant.round_no = 0
            grade = 0
        nr_contestants = len(contestants)
        print(type(nr_contestants))
        print(type(contest_series))
        for i in range(0, nr_contestants):
            contestants[i].series_no = (i+1) % contest_series + 1

        db.session.commit()
        return redirect(url_for('main.index'))

    return redirect(url_for('main.add_contestant_post'))
