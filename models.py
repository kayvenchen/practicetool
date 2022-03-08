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
    image = db.Column(db.Text, nullable=False, default = "default.jpg")
    email = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, default = datetime.utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User{}>'.format(self.username)

class Chat(db.Model):
    __tablename__ = 'Chat'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, nullable=False)

class Chat_Line(db.Model):
    __tablename__ = 'Chat_Line'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    chat_id = db.Column(db.Integer, ForeignKey('Chat.id'), nullable=False)
    reply_to = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow, nullable=False)


class File(db.Model):
    __tablename__ = 'File'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    Chat_Line_id = db.Column(db.Integer, ForeignKey('Chat_Line.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    path = db.Column(db.Text, nullable=False)


class Message(db.Model):
    __tablename__ = 'Message'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    Chat_Line_id = db.Column(db.Integer, ForeignKey('Chat_Line.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)


class Seen(db.Model):
    __tablename__ = 'Seen'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    chat_id = db.Column(db.Integer, ForeignKey('Chat.id'), nullable=False)
    seen = db.Column(db.Boolean, nullable=False)

class UserChat(db.Model):
    __tablename__ = 'ChatUser'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    uid = db.Column(db.Integer, ForeignKey('User.id'), nullable=False)
    cid = db.Column(db.Integer, ForeignKey('Chat.id'), nullable=False)

class Friendship(db.Model):
    __tablename__ = 'Friendship'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user1_id = db.Column(db.Integer, nullable=False)
    user2_id = db.Column(db.Integer, nullable=False)
    relationship_type_id = db.Column(db.Integer, nullable=False)
