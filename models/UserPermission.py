from .base import db
import datetime

class UserPermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.id'), nullable=False)
    sub_module_id = db.Column(db.Integer, db.ForeignKey('sub_module.id'), nullable=False)
    is_allowed = db.Column(db.Boolean, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)