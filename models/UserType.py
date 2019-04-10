from .base import db
import datetime

class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    users = db.relationship('User', backref='user_type', lazy=True)
    user_permissions = db.relationship('UserPermission', backref='user_type', lazy=True)
