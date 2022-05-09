from unicodedata import name
from sqlalchemy import ForeignKey
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User{}>'.format(self.username)

class Type(db.Model):
    __tablename__ = 'Type'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.String, primary_key=True, nullable=False)

class Diary(db.Model):
    __tablename__ = 'Diary'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    title = db.Column(db.String)

class Exercise(db.Model):
    __tablename__ = 'Exercise'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    is_public = db.Column(db.Boolean, nullable=False)

class Entry(db.Model):
    __tablename__ = 'Entry'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.Text)

class DiaryExercise(db.Model):
    __tablename__ = 'DiaryExercise'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    diary_id = db.Column(db.Integer, ForeignKey('Diary.id'))
    exercise_id = db.Column(db.Integer, ForeignKey('Exercise.id'))
