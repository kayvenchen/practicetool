from unicodedata import name
from sqlalchemy import ForeignKey
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship

# classes objects in user model
class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    diary = relationship('Diary', back_populates='user',
                         cascade="all, delete-orphan")
    entries = relationship('Entry', back_populates='user',
                           cascade="all, delete-orphan")

    def set_password(self, password_hash):
        self.password_hash = generate_password_hash(password_hash)

    def check_password(self, password_hash):
        return check_password_hash(self.password_hash, password_hash)

    def __repr__(self):
        return '<User{}>'.format(self.email)


# classes objects in Diary model
class Diary(db.Model):
    __tablename__ = 'Diary'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    title = db.Column(db.String)
    user = relationship('User', back_populates='diary')
    entries = relationship('Entry', back_populates='diary',
                           cascade="all, delete-orphan",
                           order_by="desc(Entry.date)")

    def __repr__(self):
        return '<Diary{}>'.format(self.title)


# entry and tag association table many-many
EntryTag = db.Table('EntryTag', db.Model.metadata,
                    db.Column('entry_id', db.Integer, db.ForeignKey('Entry.id')
                              ),
                    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id')))


# classes objects in Entry model
class Entry(db.Model):
    __tablename__ = 'Entry'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    diary_id = db.Column(db.Integer, ForeignKey('Diary.id'), nullable=False)
    date = db.Column(db.Date)
    notes = db.Column(db.Text)

    user = relationship('User', back_populates='entries')
    diary = relationship('Diary', back_populates='entries')
    tags = relationship('Tag', secondary=EntryTag, back_populates='entries',
                        order_by="Tag.name")

    def __repr__(self):
        return '<Entry{}>'.format(self.date)


# classes objects in Tag model
class Tag(db.Model):
    __tablename__ = 'Tag'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    name = db.Column(db.String)

    entries = relationship('Entry', secondary=EntryTag, back_populates='tags')

    def __repr__(self):
        return '<Tag{}>'.format(self.name)
