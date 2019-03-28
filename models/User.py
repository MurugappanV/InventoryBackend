from .base import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    user_logs = db.relationship('OrderLog', backref='user', lazy=True)
    user_sessions = db.relationship('UserSession', backref='user', lazy=True)
    user_stocks = db.relationship('Stock', backref='user', lazy=True)

    def getPermission(self):
        return PERMISSIONS[self.user_type]

    def getType(self):
        return USER_TYPE[self.user_type]

USER_TYPE = {
    1: "admin",
    2: "manager",
    3: "seller",
    4: "viewer",
    5: "maintainer"
}

PERMISSIONS = {
    1: {
        "order": {
            "add": True,
            "view": True,
            "edit": True,
            "bill": True,
            "send": True,
            "cancel": True,
            "close": True
        },
        "stock": {
            "add": True,
            "view": True,
            "update": True
        },
        "user": {
            "add": True,
            "view": True,
            "update": True
        }
    },
    3: {
        "order": {
            "add": True,
            "view": True,
            "edit": True,
            "bill": False,
            "send": False,
            "cancel": True,
            "close": False
        },
        "stock": {
            "add": False,
            "view": True,
            "update": False
        },
        "user": {
            "add": False,
            "view": False,
            "update": False
        }
    },
    2: {
        "order": {
            "add": False,
            "view": True,
            "edit": False,
            "bill": True,
            "send": True,
            "cancel": False,
            "close": False
        },
        "stock": {
            "add": True,
            "view": True,
            "update": True
        },
        "user": {
            "add": False,
            "view": False,
            "update": False
        }
    },
    4: {
        "order": {
            "add": False,
            "view": True,
            "edit": False,
            "bill": False,
            "send": False,
            "cancel": False,
            "close": False
        },
        "stock": {
            "add": False,
            "view": True,
            "update": False
        },
        "user": {
            "add": False,
            "view": False,
            "update": False
        }
    },
    5: {
        "order": {
            "add": False,
            "view": True,
            "edit": False,
            "bill": False,
            "send": False,
            "cancel": False,
            "close": False
        },
        "stock": {
            "add": False,
            "view": True,
            "update": False
        },
        "user": {
            "add": False,
            "view": False,
            "update": False
        }
    }
}