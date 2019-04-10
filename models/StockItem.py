from .base import db

class StockItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    ordered = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, nullable=False)
    misc = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    inspections = db.relationship('InspectionItem', backref='stock_item', lazy=True)
    stock_order_items = db.relationship('OrderStockItem', backref='stock_item', lazy=True)
