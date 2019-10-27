from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    type_user = db.Column(db.Integer) # 0 - admin, 1 - organizator 2 - juriu


class Contestant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)
    age = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    round_no = db.Column(db.Integer)
    series_no = db.Column(db.Integer)
    grade = db.Column(db.Integer)





    

