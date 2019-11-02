from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    type_user = db.Column(db.Integer) # 0 - admin, 1 - organizator 2 - juriu 3 - anything


class Contestant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    age = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    round_no = db.Column(db.Integer)
    series_no = db.Column(db.Integer)
    grade = db.Column(db.Integer)

class JuryVoted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jury_name = db.Column(db.String(1000))
    contestant_name = db.Column(db.String(1000))

class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    rounds = db.Column(db.Integer)
    category1 = db.Column(db.String(1000))
    category2 = db.Column(db.String(1000))
    current_rounds_junior = db.Column(db.Integer)
    current_rounds_senior = db.Column(db.Integer)
    procent1 = db.Column(db.Integer)
    procent2 = db.Column(db.Integer)





    

