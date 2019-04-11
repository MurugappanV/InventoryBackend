from .base import db
import datetime

class StockStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    stocks = db.relationship('Stock', backref='stock_status', lazy=True)
