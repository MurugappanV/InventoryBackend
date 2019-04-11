from .base import db
import datetime

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer,  db.ForeignKey('stock_status.id'), nullable=False)
    other_details = db.Column(db.String(255), nullable=False)
    seller_address_id = db.Column(db.Integer, db.ForeignKey('seller_address.id'), nullable=False)
    stock_no = db.Column(db.String(16), nullable=False)
    bill_no = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    items = db.relationship('StockItem', backref='stock', lazy=True)
    logs = db.relationship('StockLog', backref='stock', lazy=True)
    other_expenses = db.relationship('StockOtherExpenses', backref='stock', lazy=True)
