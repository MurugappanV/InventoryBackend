from base import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    other_details = db.Column(db.String(255), nullable=False)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailer.id'), nullable=False)
    order_no = db.Column(db.String(16), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    order_logs = db.relationship('OrderLog', backref='order', lazy=True)
