from .base import db
import datetime

class SubGroupHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_group_id = db.Column(db.Integer, db.ForeignKey('sub_group.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, nullable=True)
    history_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
