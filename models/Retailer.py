from base import db

class Retailer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(64), nullable=False)
    gstin_no = db.Column(db.String(24), nullable=True)
    orders = db.relationship('Order', backref=db.backref('retailer', lazy='joined'), lazy=True)
