from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    conversations = db.relationship('Conversation', backref='chat_session', lazy=True)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'user' or 'ai'
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

