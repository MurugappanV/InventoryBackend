from base import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    user_logs = db.relationship('OrderLog', backref='user', lazy=True)
    user_sessions = db.relationship('UserSession', backref='user', lazy=True)
    user_stocks = db.relationship('Stock', backref='user', lazy=True)