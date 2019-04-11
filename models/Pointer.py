from .base import db
import datetime

class Pointer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
