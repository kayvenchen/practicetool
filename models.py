from unicodedata import name
from sqlalchemy import ForeignKey
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship


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


class Diary(db.Model):
    __tablename__ = 'Diary'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    title = db.Column(db.String)

    entries = relationship('Entry', back_populates='diary')

class Entry(db.Model):
    __tablename__ = 'Entry'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    diary_id = db.Column(db.Integer, ForeignKey('Diary.id'), nullable=False)
    date = db.Column(db.Date)
    notes = db.Column(db.Text)

    diary = relationship('Diary', back_populates='entries')
    activities = relationship('Activity', back_populates='entry')


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    entry_id = db.Column(db.Integer, ForeignKey('Entry.id'), nullable=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    entry = relationship('Entry', back_populates='activities')
