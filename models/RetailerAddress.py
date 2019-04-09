from .base import db
import datetime

class RetailerAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailer.id'), nullable=False)
    delivery_name = db.Column(db.String(128), nullable=False)
    street_number = db.Column(db.String(255), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    locality = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(16), nullable=False)
    delivery_phone_no = db.Column(db.String(64), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref=db.backref('retailer_address'), lazy=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
