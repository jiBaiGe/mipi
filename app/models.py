from datetime import datetime
import json
from flask_login import UserMixin
from app.db import db


class AccssRecord(db.Model):
    __tablename__ = 'access_record'
    id = db.Column(db.Integer, primary_key=True)
    comment_time = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(500), nullable=False)
    action = db.Column(db.String(500),  nullable=False)
    action_times = db.Column(db.String(500),  nullable=False)

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique=True, index=True)
    level = db.Column(db.Integer)
    info = db.Column(db.String(500))
    hash_password = db.Column(db.String(200))
    register_time = db.Column(db.DateTime, default=datetime.now)

# class AutomanComments(db.Model):
#     __tablename__ = 'automan_comments'
#     id = db.Column(db.Integer, primary_key=True)
#     comment_time = db.Column(db.DateTime, default=datetime.now)
#     username = db.Column(db.String(500))
#     content = db.Column(db.String(500))
#     module = db.Column(db.String(500))
#     tag = db.Column(db.String(500))
#     reply = db.Column(db.String(500))
#     like = db.Column(db.String(1000))