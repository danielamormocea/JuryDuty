#from app import app
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask import Blueprint
from flask_login import login_required, current_user
from .models import User, Contestant, JuryVoted, Contest
from . import db
import random
import copy

routes = Blueprint('main', __name__)
contest_rounds = 1
#contest_series = 3
categories = []
last_round = -1
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
    if Contest.query.all() == []:
        flash("No active contest")
        return redirect(url_for('main.index'))
    contest = Contest.query.all()[0]
    cats.append(contest.category1)
    cats.append(contest.category2)
    if current_user.is_authenticated == True:
        
        cts = Contestant.query.filter_by(name=name).first()
        if (cts.age < 25 and contest.active_round == 0) or (cts.age >= 25 and contest.active_round == 1):
            if current_user.type_user == 2 and (Contestant.query.filter_by(name=name).first()).round_no != -1\
                    and JuryVoted.query.filter_by(jury_name=current_user.name, contestant_name=name).all() == []:
                show_rating = 1
    return render_template('index.html', contestants = contestants, show_rating=show_rating, vote_contestant=name, categories=cats, contestName=contest.name, contestActive=contest.active_round, last_round=last_round)


@routes.route('/', methods=['GET'])
def index():
    global jury_no
    global last_round
    print(last_round)
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
    if Contest.query.all() == []:
        #flash("No active contest")
        return render_template('profile.html')
    contest = Contest.query.all()[0]
    cats.append(contest.category1)
    cats.append(contest.category2)
    print(contest.name)
    return render_template('index.html', contestants = contestants, categories=cats, contestName=contest.name, contestActive=contest.active_round, last_round=last_round)

@routes.route('/', methods=['POST'])
def index_post():
    global last_round
    print(last_round)
    contestants = Contestant.query.all()
    if Contest.query.all() == []:
        #flash("No active contest")
        return render_template('profile.html')
    contestants.sort(key=lambda x: x.grade, reverse=True)
    if request.form.get('winners') == 'winners':
        if last_round == 0:
            contestants = list(filter(lambda x : x.series_no == 0 and x.round_no != -1, contestants))
        if last_round == 1:
            contestants = list(filter(lambda x : x.series_no == 1 and x.round_no != -1, contestants))
        print(contestants)
        if last_round == 0:
            return render_template('winners.html', juniors=contestants, current_series= current_series)
        elif last_round == 1:
            return render_template('winners.html', seniors=contestants, current_series= current_series)

    contestants = Contestant.query.all()
    cats = []
    
    contest = Contest.query.all()[0]
    cats.append(contest.category1)
    cats.append(contest.category2)
    if (request.form.get('cancel') == "cancel_vote"):
        return render_template('index.html', contestants = contestants, categories=cats, contestName=contest.name, contestActive=contest.active_round, last_round=last_round)

    grade1 = 0
    grade2 = 0

    if ('rate' in request.form.to_dict(flat=False)):
        grade1 = (contest.procent1 / 100) * int(request.form.to_dict(flat=False)['rate'][0])/(jury_no)
    if ('rate2' in request.form.to_dict(flat=False)):
        grade2 = (contest.procent2 / 100) * int(request.form.to_dict(flat=False)['rate2'][0])/(jury_no)

    update_contestant = Contestant.query.filter_by(name=request.form.get('contestant_vote')).first()
    update_contestant.grade += grade1 + grade2
    new_jury_voted = JuryVoted(id=random.randint(9999, 100000), jury_name=current_user.name, contestant_name=request.form.get('contestant_vote'))
    db.session.add(new_jury_voted)
    db.session.commit()


    return redirect(url_for('main.index'))


@routes.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)

data_organize={}
@routes.route ('/organize', methods=['GET'])
def organize():
    global categories
    global data_organize
    global contest_name
    global contest_rounds
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
    global percents
    return render_template('organize.html', categories = categories, percents= percents, contest_name = "", contest_rounds = "")


@routes.route ('/organize', methods=['POST'])
def organize_post():
    global contest_name 
    contest_name = request.form.get('contest_name')
    global contest_rounds 
    contest_rounds = int(request.form.get('round_no'))
    current_round = 1
    
    global categories
    global percents
    global data_organize
    calcPercent = 0
    validateNrCategories = 0
    categories_names = []
    percentsToInsert = []
    for x in categories:
        if request.form.get(x['name']) == None:
            x['value'] = False
        strr = x['name'] + 'pr'

        if x['value'] != False:
            validateNrCategories += 1
            x['percent'] = int(request.form.get(strr))
            calcPercent += x['percent']
            categories_names.append(x['name'])
            percentsToInsert.append(int(request.form.get(strr)))

    print(categories)
    print('calcPercent' + str(calcPercent))
    print('validateNrCategories' + str(validateNrCategories))
    if validateNrCategories != 2:
        flash('Wrong number of categories')
        for x in categories:
            x['percent'] = 0
            x['value'] = True
        return render_template('organize.html', categories=categories, percents=percents, contest_name=contest_name,
                               contest_rounds=contest_rounds)
    else:
        if calcPercent != 100:
            flash('Different than 100%')
            for x in categories:
                x['percent'] = 0
                x['value'] = True
            return render_template('organize.html', categories=categories, percents=percents, contest_name=contest_name,
                                   contest_rounds=contest_rounds)
        else:
            contests = Contest.query.all()
            for contest in contests:
                db.session.delete(contest)
            db.session.commit()
            print(str(contest_name) + str(contest_rounds) + str(categories_names) + str(percentsToInsert))
            new_contest = Contest(id=random.randint(1, 100000), name=contest_name, rounds=contest_rounds,
                                  category1=categories_names[0], category2=categories_names[1], current_rounds_junior=0,
                                  current_rounds_senior=0, procent1=percentsToInsert[0], procent2=percentsToInsert[1])
            jures = JuryVoted.query.all()
            for jure in jures:
                db.session.delete(jure)
            print(new_contest)
            db.session.add(new_contest)
            db.session.commit()
    
            contestants = Contestant.query.all()
            if (len(contestants) != 0):
                for cts in contestants:
                    db.session.delete(cts)
                db.session.commit()
            return redirect(url_for('main.add_contestant'))


@routes.route('/add_contestant' , methods=['GET'])
def add_contestant():
    return render_template('add_contestant.html')


@routes.route('/add_contestant' , methods=[ 'POST'])
def add_contestant_post():
    global i
    if Contest.query.all() == []:
        flash("No active contest")
        return redirect(url_for('main.index'))
    contest = Contest.query.all()[0]

    if request.form.get('name_contestant') != None:
        contestant_name = request.form.get('name_contestant')
        age = request.form.get('age')
        description = request.form.get('description')
        i = random.randint(1000, 9999)
        new_contestant = Contestant( id = i, name = contestant_name.strip(), age = int(age), description = description, round_no = 0, series_no = 0, grade = 0)

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
    if Contest.query.all() == []:
        flash("No active contest")
        return redirect(url_for('main.index'))
    contest = Contest.query.all()[0]
    if contest.current_rounds_junior == contest.rounds and contest.current_rounds_senior == contest.rounds and contest.active_round == -1:
        flash("GAME HAS ENDED")
        db.session.delete(contest)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        return render_template('game_opt.html', contestants=contestants, current_round = [contest.current_rounds_junior, contest.current_rounds_senior])

@routes.route('/game_opt', methods=['POST'])
def game_opt_post():
    global current_round
    global current_series
    global last_round

    game = request.form.get('game')
    print(game)
    if (Contest.query.all() == []):
        flash("No contest")
        return redirect(url_for('main.index'))
    contest = Contest.query.all()[0]
    contestants = Contestant.query.all()
    jury = User.query.filter_by(type_user=2)

    if request.form.get('disq') != None:
        disq_contestant = request.form.get('disq')
        Contestant.query.filter_by(name=disq_contestant).delete()
        db.session.commit()
        contestants = Contestant.query.all()
        return render_template('game_opt.html', contestants=contestants, current_round = [contest.current_rounds_junior, contest.current_rounds_senior])
    
    if game == 'start_game':
        print(contest.active_round)
        if contest.active_round != -1:
            flash("A round is still in progress!")
            return render_template('game_opt.html', contestants=contestants, current_round = [contest.current_rounds_junior, contest.current_rounds_senior])
        current_series = request.form.get('select_series')
       
        seniors = Contestant.query.filter(Contestant.age >= 25, Contestant.round_no != -1).all()
        juniors = Contestant.query.filter(Contestant.age < 25, Contestant.round_no != -1).all()
        print(juniors)

        if current_series == 'senior' and contest.current_rounds_senior < contest.rounds and seniors != []:
            contest.active_round = 1
            last_round = -1
            contest.current_rounds_senior += 1
            #trecem prin toti seniorii si facem +1
            for contestant in contestants:
                contestant.grade = 0
                if contestant.age >= 25 and contestant.round_no != -1:
                    contestant.round_no = contest.current_rounds_senior
                    JuryVoted.query.filter_by(contestant_name=contestant.name).delete()

        elif current_series == 'junior' and contest.current_rounds_junior < contest.rounds and juniors != []:
            contest.active_round = 0
            last_round = -1
            contest.current_rounds_junior += 1
            for contestant in contestants:
                contestant.grade = 0
                if contestant.age < 25  and contestant.round_no != -1:
                    contestant.round_no = contest.current_rounds_junior
                    JuryVoted.query.filter_by(contestant_name=contestant.name).delete()
        else:
            flash('The selected series round has come to an end.')
            return render_template('game_opt.html', contestants=contestants, current_round = [contest.current_rounds_junior, contest.current_rounds_senior])
        db.session.commit()
        return redirect(url_for('main.index'))

    elif game == 'finish_game':
        last_round = contest.active_round
      
        if contest.active_round == -1:
            flash("No round is in progress")
            return render_template('game_opt.html', contestants=contestants, current_round = [contest.current_rounds_junior, contest.current_rounds_senior])
        current_series = request.form.get('select_series')
        if current_series == 'junior' and contest.active_round == 1 or current_series == 'senior' and contest.active_round == 0:
            flash('Wrong series to be finished.')
            return render_template('game_opt.html', contestants=contestants, current_round = [contest.current_rounds_junior, contest.current_rounds_senior])
        contest.active_round = -1
        contestants = Contestant.query.all()
        print(contestants)
        for cts in contestants:
            
            if cts.round_no != -1 and cts.grade < 2.5 and ((cts.series_no == 0 and current_series == 'junior') or (cts.series_no == 1 and current_series == 'senior')):
                cts.round_no = -1
                
            for judge in jury:
                new_jury_voted = JuryVoted(id=random.randint(1, 1000000) ,jury_name=judge.name, contestant_name=cts.name)
                db.session.add(new_jury_voted)
        
        seniors = Contestant.query.filter(Contestant.age >= 25, Contestant.round_no != -1).all()
        juniors = Contestant.query.filter(Contestant.age < 25, Contestant.round_no != -1).all()
        if contest.rounds == contest.current_rounds_junior and contest.rounds == contest.current_rounds_senior or \
            len(seniors) <= 1 and len(juniors) <=  1:

            seniors.sort(key=lambda x: x.grade, reverse=True)
            juniors.sort(key=lambda x: x.grade, reverse=True)
            contest = Contest.query.all()[0]
            db.session.delete(contest)
            db.session.commit()
            return render_template('winners.html', juniors = juniors, seniors = seniors, final = True)


        ccontestants = copy.deepcopy(contestants)
        ccontestants.sort(key=lambda x: x.grade, reverse=True)
        """for ct in contestants:
            ct.grade = 0"""
        db.session.commit()

        if current_series == 'junior':
            ccontestants = list(filter(lambda x : x.series_no == 0 and x.round_no != -1, ccontestants))
        if current_series == 'senior':
            ccontestants = list(filter(lambda x : x.series_no == 1 and x.round_no != -1, ccontestants))
        print(ccontestants)
        if current_series == 'junior':
            return render_template('winners.html', juniors=ccontestants, current_series= current_series)
        elif current_series == 'senior':
            return render_template('winners.html', seniors=ccontestants, current_series= current_series)



# grade tre sa se faca 0 candva

@routes.route('/winners', methods=['GET'])
def winners():
    return render_template('winners.html')

@routes.route('/winners', methods=['POST'])
def winners_post():
    ret = request.form.get('return')
    print(ret)
    if ret == 'return':
        print(ret)
        return redirect(url_for('main.index'))
    
@routes.route('/jury_opt', methods=['GET'])
def jury_opt():
    juries = User.query.filter_by(type_user=2).all()
    return render_template('jury_opt.html', juries=juries)

@routes.route('/jury_opt', methods=['POST'])
def jury_opt_post():
    
    if request.form.get('kick') != None:
        disq_jury = request.form.get('kick')
        print(disq_jury)
        User.query.filter_by(name=disq_jury).delete()
        db.session.commit()
        juries = User.query.filter_by(type_user=2).all()
        return render_template('jury_opt.html', juries=juries)