from game import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email_address = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    highscore = db.Column(db.Integer(), default=0)
    scores = db.relationship('Scores')


class Scores(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    score = db.Column(db.Integer())
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))



class Round(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    computer = db.Column(db.Integer(), default=0)
    user = db.Column(db.Integer(), default=0)

