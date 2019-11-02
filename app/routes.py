#from app import app
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask import Blueprint
from flask_login import login_required, current_user
from .models import User, Contestant, JuryVoted, Contest
from . import db
import random

routes = Blueprint('main', __name__)

contest_name = ""
contest_rounds = 4
#contest_series = 3
categories = []

jury_no = 1

current_round = {'junior':0, 'senior':0}
current_series = ""

percents = [10, 25, 30, 50, 75]

@routes.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('./static/css/', path)


# TODO: sa apara categoria la rating!!!
@routes.route('/vote/<string:name>', methods=['GET'])
def vote(name):
    contestants = Contestant.query.all()
    cats = []
    show_rating = 0
    contest = Contest.query.all().first()
    cats.append(contest.category1)
    cats.append(contest.category2)
    if current_user.type_user == 2 and (Contestant.query.filter_by(name=name).first()).round_no != -1\
            and JuryVoted.query.filter_by(jury_name=current_user.name, contestant_name=name).scalar() is None:
        show_rating = 1
    return render_template('index.html', contestants = contestants, show_rating=show_rating, vote_contestant=name, categories=cats)


@routes.route('/', methods=['GET'])
def index():
    global jury_no
    jury_no = User.query.filter_by(type_user=2).count()
    contestants = Contestant.query.all()
    #if current_user:
     #   user = User.query.filter_by(name=current_user.name).all()
    # contestans = {<Contestant 1>, <Contestant 12>, <Contestant 2> ....}
    # contestant[0] -> Contestant 1
    # contestant[0].age, contestant[0].name ... etc
    # ex: for contestant in contestants:
    #       print contestant.age

    cats = []
    contest = Contest.query.all().first()
    cats.append(contest.category1)
    cats.append(contest.category2)
    return render_template('index.html', contestants = contestants, categories=cats, contestName=contest_name)

@routes.route('/', methods=['POST'])
def index_post():

    contestants = Contestant.query.all()
    cats = []

    contest = Contest.query.all().first()
    cats.append(contest.category1)
    cats.append(contest.category2)
    if (request.form.get('cancel') == "cancel_vote"):
        return render_template('index.html', contestants = contestants, categories=cats, contestName=contest_name)

    grade1 = 0
    grade2 = 0

    if ('rate' in request.form.to_dict(flat=False)):
        grade1 = contest.procent1[0] * int(request.form.to_dict(flat=False)['rate'][0])/(2*jury_no)
    if ('rate2' in request.form.to_dict(flat=False)):
        grade2 = contest.procent2[1] * int(request.form.to_dict(flat=False)['rate2'][0])/(2*jury_no)

    update_contestant = Contestant.query.filter_by(name=request.form.get('contestant_vote')).first()
    update_contestant.grade += grade1 + grade2
    new_jury_voted = JuryVoted(id=random.randint(9999, 100000), jury_name=current_user.name, contestant_name=request.form.get('contestant_vote'))
    db.session.add(new_jury_voted)
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
    current_round = 1

    contestants = Contestant.query.all()
    if (len(contestants) != 0):
        for cts in contestants:
            db.session.delete(cts)
        db.session.commit()
    global categories
    global percents
    calcPercent = 0
    categories_names = []
    percents = []
    for x in categories:
        if request.form.get(x['name']) == None:
            x['value'] = False
        strr = x['name'] + 'pr'

        if x['value'] != False:
            x['percent'] = int(request.form.get(strr))
            calcPercent += x['percent']
            categories_names.append(x['name'])
            percents.append(int(request.form.get(strr)))

    #print(categories)

    if calcPercent > 100:
        flash('More than 100%')
        return render_template('organize.html', categories=categories, percents=percents)
    else:
        print(str(contest_name) + str(contest_rounds) + str(categories_names) + str(percents))
        new_contest = Contest(id=random.randint(1, 100000), name=contest_name, rounds=contest_rounds,
                              category1=categories_names[0], category2=categories_names[1], current_rounds_junior=0,
                              current_rounds_senior=0, procent1=percents[0], procent2=percents[1])
        db.session.add(new_contest)
        db.session.commit()
        return redirect(url_for('main.add_contestant'))


@routes.route('/add_contestant' , methods=['GET'])
def add_contestant():
    return render_template('add_contestant.html')


@routes.route('/add_contestant' , methods=[ 'POST'])
def add_contestant_post():
    global i
    contest = Contest.query.all().first()

    if request.form.get('name_contestant') != None:
        contestant_name = request.form.get('name_contestant')
        age = request.form.get('age')
        description = request.form.get('description')
        i = random.randint(1000, 9999)
        new_contestant = Contestant( id = i, name = contestant_name, age = int(age), description = description, round_no = 0, series_no = 0, grade = 0)

        db.session.add(new_contestant)
        db.session.commit()

    if request.form.get('finish') == "Finish":
        contestants = Contestant.query.all()
        if len(contestants) != 0:
            for contestant in contestants:
                contestant.round_no = 0
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
    contest = Contest.query.all().first()
    if contest.current_rounds_junior == contest.rounds and contest.current_rounds_senior == contest.rounds:
        flash("GAME HAS ENDED")
        db.session.delete(contest)
        db.session.commit()
    else:
        return render_template('game_opt.html', contestants=contestants, current_round = [contest.current_rounds_junior, contest.current_rounds_senior])

@routes.route('/game_opt', methods=['POST'])
def game_opt_post():
    global current_round
    global current_series
    game = request.form.get('game')
    print(game)
    contest = Contest.query.all().first()

    if request.form.get('disq') != None:
        disq_contestant = request.form.get('disq')
        Contestant.query.filter_by(name=disq_contestant).delete()
        db.session.commit()
        contestants = Contestant.query.all()
        return render_template('game_opt.html', contestants=contestants, current_round = [contest.current_rounds_junior, contest.current_rounds_senior])
    if game == 'start_game':
        current_series = request.form.get('select_series')
        if current_series is 'senior':
            contest.current_rounds_senior += 1
        else:
            contest.current_rounds_junior += 1

        return redirect(url_for('main.index'))
    elif game == 'finish_game':
        contestants = Contestant.query.all()
        for cts in contestants:
            if cts.round_no != -1 and cts.grade < 2.5 + cts.round_no*(1.8/contest.rounds):
                cts.round_no = -1
                db.session.commit()
        return render_template('winners.html', contestants=contestants)

@routes.route('/winners', methods=['GET'])
def winners():
    return render_template('winnders.html')
    
