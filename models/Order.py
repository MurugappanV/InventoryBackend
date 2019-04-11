from .base import db
import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer,  db.ForeignKey('order_status.id'), nullable=False)
    other_details = db.Column(db.String(255), nullable=False)
    retailer_address_id = db.Column(db.Integer, db.ForeignKey('retailer_address.id'), nullable=False)
    order_no = db.Column(db.String(16), nullable=False)
    bill_no = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    order_logs = db.relationship('OrderLog', backref='order', lazy=True)
    expenses = db.relationship('OrderExpenses', backref='order', lazy=True)
    other_expenses = db.relationship('OrderOtherExpenses', backref='order', lazy=True)
    returns = db.relationship('OrderReturn', backref='order', lazy=True)
