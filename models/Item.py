from .base import db
import datetime

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    bill_name = db.Column(db.String(128), nullable=False)
    available = db.Column(db.Integer, nullable=False)
    ordered = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, nullable=False)
    misc = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    packcount = db.Column(db.Integer, nullable=False)
    gst_percent = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    sub_group_id = db.Column(db.Integer, db.ForeignKey('sub_group.id'), nullable=False)
    item_orders = db.relationship('OrderItem', backref='item', lazy=True)
    item_stocks = db.relationship('StockItem', backref='item', lazy=True)
    # history = db.relationship('ItemHistory', backref='item', lazy=True)
