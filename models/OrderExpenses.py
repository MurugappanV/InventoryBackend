from .base import db
import datetime

class OrderExpenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    sales_commission = db.Column(db.Integer, nullable=False)
    manager_commission = db.Column(db.Integer, nullable=False)
    shipping = db.Column(db.Integer, nullable=False)
    packaging = db.Column(db.Integer, nullable=False)
    bill_include_packing = db.Column(db.Boolean, default=False)
    bill_include_shipping = db.Column(db.Boolean, default=False)