from .base import db
import datetime

class OrderReturn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    other_details = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    items = db.relationship('OrderReturnItem', backref='order_item', lazy=True)
