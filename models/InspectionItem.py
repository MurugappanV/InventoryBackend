from .base import db
import datetime

class InspectionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    stock_item_id = db.Column(db.Integer, db.ForeignKey('stock_item.id'), nullable=False)
    available = db.Column(db.Integer, nullable=False)
    ordered = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, nullable=False)
    misc = db.Column(db.Integer, nullable=False)