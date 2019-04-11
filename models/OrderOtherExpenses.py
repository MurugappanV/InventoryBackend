from .base import db
import datetime

class OrderOtherExpenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    expense = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    include_in_bill = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)