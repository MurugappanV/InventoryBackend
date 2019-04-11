from .base import db
import datetime

class OrderReturnItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_return_id = db.Column(db.Integer, db.ForeignKey('order_return.id'), nullable=False)
    order_item_id = db.Column(db.Integer, db.ForeignKey('order_item.id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
