from .base import db
import datetime

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    other_details = db.Column(db.String(255), nullable=False)
    stock_no = db.Column(db.String(16), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    stock_items = db.relationship('StockItem', backref='stock', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
