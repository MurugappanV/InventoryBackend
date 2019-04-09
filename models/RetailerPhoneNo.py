from .base import db
import datetime

class Retailer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailer.id'), nullable=False)
    phone_no = db.Column(db.String(24), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
