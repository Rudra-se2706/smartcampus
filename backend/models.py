from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role     = db.Column(db.String(20), default='student')
    created  = db.Column(db.DateTime, default=datetime.utcnow)

class Notice(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

class StudyGroup(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    subject    = db.Column(db.String(100), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created    = db.Column(db.DateTime, default=datetime.utcnow)

class ChatMessage(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('study_group.id'))
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
    message  = db.Column(db.Text, nullable=False)
    sent_at  = db.Column(db.DateTime, default=datetime.utcnow)

class LoginAttempt(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(120))
    ip_address = db.Column(db.String(50))
    success    = db.Column(db.Boolean)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)