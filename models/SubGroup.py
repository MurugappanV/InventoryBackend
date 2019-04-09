from .base import db
import datetime

class SubGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    items = db.relationship('Item', backref='sub_group', lazy=True)
    history = db.relationship('SubGroupHistory', backref='sub_group', lazy=True)
