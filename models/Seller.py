from .base import db
import datetime

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    gstin_no = db.Column(db.String(24), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    addresses = db.relationship('SellerAddress', backref=db.backref('seller'), lazy=True)
    phone_nos = db.relationship('SellerPhoneNo', backref=db.backref('seller'), lazy=True)
