from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, logout_user, login_required
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():


    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))



@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    type_user = 3
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    
    user = User.query.filter_by(name=name).first()
    if user:
        flash('Username already taken')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), type_user=type_user)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/give_perm', methods=['GET'])
def give_perm():
    return render_template('give_perm.html')


@auth.route('/give_perm', methods=['POST'])
def give_perm_post():
    
    name = request.form.get('username')
    global jury_no
    print(request.form.get('jury'))
    if request.form.get('jury') == 'on':
        user = User.query.filter_by(name=name).first()
        if user is None:
            flash("User does not exist")
            return render_template('give_perm.html')
        #print("before " + str(user.name) + " " + str(user.type_user))
        user.type_user = 2
        print(user)
    elif request.form.get('organizer') == 'on':
        user = User.query.filter_by(name=name).first()
        print("before " + str(user.name) + " " + str(user.type_user))
        user.type_user = 1
    elif request.form.get('admin') == 'on':
        user = User.query.filter_by(name=name).first()
        print("before " + str(user.name) + " " + str(user.type_user))
        user.type_user = 0

    print(str(user.name) + " " + str(user.type_user))
    db.session.commit()
    return redirect(url_for('auth.give_perm'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
