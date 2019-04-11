from .base import db
import datetime

class SellerAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    delivery_name = db.Column(db.String(128), nullable=False)
    street_number = db.Column(db.String(255), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    locality = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(16), nullable=False)
    delivery_phone_no = db.Column(db.String(64), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    stocks = db.relationship('Stock', backref=db.backref('seller_address'), lazy=True)
