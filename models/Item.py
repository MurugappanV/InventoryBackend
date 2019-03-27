from base import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    bill_name = db.Column(db.String(128), nullable=False)
    available = db.Column(db.Integer, nullable=False)
    ordered = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, nullable=False)
    misc = db.Column(db.Integer, nullable=False)
    sub_group_id = db.Column(db.Integer, db.ForeignKey('sub_group.id'), nullable=False)
    item_orders = db.relationship('OrderItem', backref='item', lazy=True)
    item_stocks = db.relationship('StockItem', backref='item', lazy=True)
