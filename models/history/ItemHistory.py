from .base import db
import datetime

class ItemHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    bill_name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    packcount = db.Column(db.Integer, nullable=False)
    gst_percent = db.Column(db.Integer, nullable=False)
    sub_group_id = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, nullable=True)
    history_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)