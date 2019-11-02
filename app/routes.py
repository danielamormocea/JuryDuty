#from app import app
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask import Blueprint
from flask_login import login_required, current_user
from .models import User, Contestant
from . import db
import random

routes = Blueprint('main', __name__)

contest_name = ""
contest_rounds = 1
contest_series = 3
categories =[]
i = 100
percents = [10, 25, 30, 50, 75]

@routes.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('./static/css/', path)


# TODO: sa apara categoria la rating!!!
@routes.route('/vote/<string:name>', methods=['GET'])
def vote(name):
    contestants = Contestant.query.all()
    cats = []
    if len(categories) != 0:
        for category in categories:
            if category['value'] == True:
                cats.append(category['name'])
    return render_template('index.html', contestants = contestants, show_rating=1, vote_contestant=name, categories=cats)


@routes.route('/', methods=['GET'])
def index():
    contestants = Contestant.query.all()
    #if current_user:
     #   user = User.query.filter_by(name=current_user.name).all()
    # contestans = {<Contestant 1>, <Contestant 12>, <Contestant 2> ....}
    # contestant[0] -> Contestant 1
    # contestant[0].age, contestant[0].name ... etc
    # ex: for contestant in contestants:
    #       print contestant.age

    cats = []
    if len(categories) != 0:
        for category in categories:
            if category['value'] == True:
                cats.append(category['name'])
    return render_template('index.html', contestants = contestants, categories=cats)

@routes.route('/', methods=['POST'])
def index_post():

    contestants = Contestant.query.all()
    cats = []
    if len(categories) != 0:
        for category in categories:
            if category['value'] == True:
                cats.append(category['name'])
    if (request.form.get('cancel') == "cancel_vote"):
        return render_template('index.html', contestants = contestants, categories=cats)

    grade1 = 0
    grade2 = 0
    if ('rate' in request.form.to_dict(flat=False)):
        grade1 = int(request.form.to_dict(flat=False)['rate'][0])/2
    if ('rate2' in request.form.to_dict(flat=False)):
        grade2 = int(request.form.to_dict(flat=False)['rate2'][0])/2
    # TODO: adaugat media notelor la contestant;
    update_contestant = Contestant.query.filter_by(name=request.form.get('contestant_vote')).first()
    update_contestant.grade = grade1 + grade2
    db.session.commit()
    return redirect(url_for('main.index'))


@routes.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)


@routes.route ('/organize', methods=['GET'])
def organize():
    global categories
    cat1 = {
        'name' : 'plating',
        'value' : True,
        'percent' : 0
    }
    cat2 = {
        'name': 'smell',
        'value': True,
        'percent' : 0
    }
    cat3 = {
        'name': 'taste',
        'value': True,
        'percent': 0
    }
    cat4 = {
        'name': 'colour',
        'value': True,
        'percent': 0
    }
    categories = [cat1, cat2, cat3, cat4]

    return render_template('organize.html', categories = categories, percents = percents)


@routes.route ('/organize', methods=['POST'])
def organize_post():
    global contest_name 
    contest_name = request.form.get('contest_name')
    global contest_rounds 
    contest_rounds = int(request.form.get('round_no'))
    global contest_series
    contest_series = int(request.form.get('series_no'))
    print(contest_series)

    global categories
    global percents
    calcPercent = 0
    for x in categories:
        if request.form.get(x['name']) == None:
            x['value'] = False
        str = x['name'] + 'pr'

        if x['value'] != False:
            x['percent'] = int(request.form.get(str))
            calcPercent += x['percent']

    print(categories)
    if calcPercent > 100:
        flash('More than 100%')
        return render_template('organize.html', categories=categories, percents=percents)
    else:
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
        i = random.randint(1000, 9999)
        new_contestant = Contestant( id = i, name = contestant_name, age = int(age), description = description, round_no = 0, series_no = 0, grade = 0)

        db.session.add(new_contestant)
        db.session.commit()

    if request.form.get('finish') == "Finish":
        print("ALALLALALAL")
        contestants = Contestant.query.all()
        if len(contestants) != 0:
            for contestant in contestants:
                contestant.round_no = contest_rounds
                if (contestant.age is None):
                    pass
                if (int(contestant.age) < 25):
                    contestant.series_no = 0
                else:
                    contestant.series_no = 1
                contestant.grade = 0
            

            db.session.commit()
        return redirect(url_for('main.index'))

    return redirect(url_for('main.add_contestant_post'))


@routes.route('/game_opt', methods=['GET'])
def game_opt():
    contestants = Contestant.query.all()

    return render_template('game_opt.html', contestants=contestants)










