from .base import db
import datetime

class OrderLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    action = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def getAction(self):
        return ACTION[self.action]

ACTION = {
    1:'CREATE_ORDER',
    2:'EDIT_ORDER',
    3:'BILL_ORDER',
    4:'SEND_ORDER',
    5:'CLOSE_ORDER',
    6:'CANCEL_ORDER'
}