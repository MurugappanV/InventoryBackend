from .base import db
import datetime

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    gst_percent = db.Column(db.Integer, nullable=False)
    gst_amount = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    is_packed = db.Column(db.Boolean, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    returnItems = db.relationship('OrderReturnItem', backref='order_item', lazy=True)
    order_stock_items = db.relationship('OrderStockItem', backref='order_item', lazy=True)
