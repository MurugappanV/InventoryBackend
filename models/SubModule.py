from .base import db
import datetime

class SubModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    user_permissions = db.relationship('UserPermission', backref='sub_module', lazy=True)
