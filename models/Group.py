from .base import db
import datetime

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    sub_groups = db.relationship('SubGroup', backref='group', lazy=True)
    # history = db.relationship('GroupHistory', backref='group', lazy=True)
