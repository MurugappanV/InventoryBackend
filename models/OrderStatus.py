from .base import db
import datetime

class OrderStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    orders = db.relationship('Order', backref='order_status', lazy=True)
