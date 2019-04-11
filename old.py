
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_expects_json import expects_json
import uuid
import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Murugappan",
    password="STQ-n6t-ZGq-fKH",
    hostname="Murugappan.mysql.pythonanywhere-services.com",
    databasename="Murugappan$Stationery",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    user_logs = db.relationship('OrderLog', backref='user', lazy=True)
    user_sessions = db.relationship('UserSession', backref='user', lazy=True)
    user_stocks = db.relationship('Stock', backref='user', lazy=True)

class Retailer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(64), nullable=False)
    gstin_no = db.Column(db.String(24), nullable=True)
    orders = db.relationship('Order', backref=db.backref('retailer', lazy='joined'), lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    other_details = db.Column(db.String(255), nullable=False)
    retailer_id = db.Column(db.Integer, db.ForeignKey('retailer.id'), nullable=False)
    order_no = db.Column(db.String(16), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    order_logs = db.relationship('OrderLog', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    other_details = db.Column(db.String(255), nullable=False)
    stock_no = db.Column(db.String(16), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    stock_items = db.relationship('StockItem', backref='stock', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class StockItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

class OrderLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    action = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    sub_groups = db.relationship('SubGroup', backref='group', lazy=True)

class SubGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    items = db.relationship('Item', backref='sub_group', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    bill_name = db.Column(db.String(128), nullable=False)
    available = db.Column(db.Integer, nullable=False)
    ordered = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, nullable=False)
    misc = db.Column(db.Integer, nullable=False)
    sub_group_id = db.Column(db.Integer, db.ForeignKey('sub_group.id'), nullable=False)
    item_orders = db.relationship('OrderItem', backref='item', lazy=True)
    item_stocks = db.relationship('StockItem', backref='item', lazy=True)

class UserSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(128), nullable=False)
    isDeleted = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Pointer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Integer, nullable=False)

ma = Marshmallow(app)

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class RetailerSchema(ma.ModelSchema):
    class Meta:
        model = Retailer

class OrderSchema(ma.ModelSchema):
    class Meta:
        model = Order

class OrderItemSchema(ma.ModelSchema):
    class Meta:
        model = OrderItem

class StockSchema(ma.ModelSchema):
    class Meta:
        model = Stock

class StockItemSchema(ma.ModelSchema):
    class Meta:
        model = StockItem

class OrderLogSchema(ma.ModelSchema):
    class Meta:
        model = OrderLog

class GroupSchema(ma.ModelSchema):
    class Meta:
        model = Group

class SubGroupSchema(ma.ModelSchema):
    class Meta:
        model = SubGroup

class ItemSchema(ma.ModelSchema):
    class Meta:
        model = Item

class UserSessionSchema(ma.ModelSchema):
    class Meta:
        model = UserSession

user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_log_schema = OrderLogSchema()
order_logs_schema = OrderLogSchema(many=True)
retailer_schema = RetailerSchema()
retailers_schema = RetailerSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)
stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)
stock_item_schema = StockItemSchema()
stock_items_schema = StockItemSchema(many=True)
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
sub_group_schema = SubGroupSchema()
sub_groups_schema = SubGroupSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
user_session_schema = UserSessionSchema()
user_sessions_schema = UserSessionSchema(many=True)

# users_schema.dump(User.query.all())
# str(uuid.uuid4())

STATUS = {
    1:'CREATED',
    2:'EDITED',
    3:'BILLED',
    4:'SEND',
    5:'CLOSED',
    6:'CANCELLED'
}

ACTION = {
    1:'CREATE_ORDER',
    2:'EDIT_ORDER',
    3:'BILL_ORDER',
    4:'SEND_ORDER',
    5:'CLOSE_ORDER',
    6:'CANCEL_ORDER'
}

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

class ControlManager:
    def login(self, name, password):
        try:
            user = User.query.filter_by(name=name).first()
            if user is None:
                return {
                    "data": None,
                    "message": "Username does not exist",
                    "status": 0
                }
            if user.password != password:
                return {
                    "data": None,
                    "message": "Username and password does not match",
                    "status": 0
                }
            user_session = UserSession(date=datetime.datetime.now(), token=str(uuid.uuid4()), isDeleted=False, user_id=user.id)
            db.session.add(user_session)
            db.session.commit()
            return {
                "data": {
                    "user_id": user_session.user_id,
                    "token": user_session.token,
                    "user_type": user.user_type,
                    "permissions": PERMISSIONS[user.user_type]
                },
                "message": "Login successfull",
                "status": 1
            }
        except Exception as e:
            db.session.rollback()
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def permissions(self, token, user_id):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None:
                return {
                    "data": None,
                    "message": "Session does not exist",
                    "status": 0
                }
            user = User.query.filter_by(id=user_id).first()
            return {
                "data": {
                    "user_type": user.user_type,
                    "permissions": PERMISSIONS[user.user_type]
                },
                "message": "success",
                "status": 1
            }
        except Exception as e:
            db.session.rollback()
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def addUser(self, token, user_id, name, password, email, user_type):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None:
                return {
                    "data": None,
                    "message": "Session does not exist",
                    "status": 0
                }
            user = User.query.filter_by(id=user_id).first()
            if user.user_type is not 1: # admin
                return {
                    "data": None,
                    "message": "Admin access needed",
                    "status": 0
                }
            new_user = User(name=name, password=password, email=email,user_type=user_type)
            db.session.add(new_user)
            db.session.commit()
            return {
                "data": {
                    "id": new_user.id,
                    "name": new_user.name,
                    "password": new_user.password,
                    "user_type": new_user.user_type
                },
                "message": "Add user successfull",
                "status": 1
            }
        except Exception as e:
            db.session.rollback()
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def updateUserType(self, token, user_id, update_user_id, user_type):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None:
                return {
                    "data": None,
                    "message": "Session does not exist",
                    "status": 0
                }
            user = User.query.filter_by(id=user_id).first()
            if user.user_type is not 1: # admin
                return {
                    "data": None,
                    "message": "Admin access needed",
                    "status": 0
                }
            update_user = User.query.filter_by(id=update_user_id).first()
            if update_user is None: # admin
                return {
                    "data": None,
                    "message": "User does not exist",
                    "status": 0
                }
            update_user.user_type=user_type
            db.session.commit()
            return {
                "data": {
                    "id": update_user.id,
                    "name": update_user.name,
                    "password": update_user.password,
                    "user_type": update_user.user_type
                },
                "message": "Update user type successfull",
                "status": 1
            }
        except Exception as e:
            db.session.rollback()
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def logout(self, token, user_id):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None:
                return {
                    "data": None,
                    "message": "Session does not exist",
                    "status": 0
                }
            user_session.isDeleted=True
            db.session.commit()
            return {
                "data": None,
                "message": "User Session Deleted",
                "status": 1
            }
        except Exception as e:
            db.session.rollback()
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def getOrders(self, token, user_id):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": None,
                    "message": "Invalid session",
                    "status": 0
                }
            ordersResult = Order.query.order_by(Order.created_date.desc()).all()
            orders = []
            for order in ordersResult:
                retailer = order.retailer
                no_of_items = OrderItem.query.filter_by(order_id=order.id, is_deleted=False).count()
                logs = []
                for log in order.order_logs:
                    logs.append({
                        "id": log.id,
                        "date": log.date,
                        "action": ACTION[log.action],
                        "name": log.user.name
                    })
                orders.append({
                    "id": order.id,
                    "retailer": {
                        "id": retailer.id,
                        "name": retailer.name,
                        "address" : retailer.address,
                        "phone_no" : retailer.phone_no,
                        "gstin_no" : retailer.gstin_no,
                    },
                    "logs": logs,
                    "status": STATUS[order.status],
                    "other_details": order.other_details,
                    "created_date": order.created_date,
                    "order_no": order.order_no,
                    "no_of_items": no_of_items
                })
            return {
                "data": {
                    "orders": orders,
                },
                "message": "success",
                "status": 1
            }
        except Exception as e:
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def getUsers(self, token, user_id):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": user_session,
                    "message": {"t": token, "u": user_id},
                    "status": 0
                }
            user = User.query.filter_by(id=user_id).first()
            if user.user_type is not 1: # admin
                return {
                    "data": None,
                    "message": "Admin access needed",
                    "status": 0
                }
            usersResult = User.query.all()
            users = []
            for user in usersResult:
                users.append({
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "password": user.password,
                    "user_type": user.user_type,
                })
            return {
                "data": {
                    "users": users,
                },
                "message": "success",
                "status": 1
            }
        except Exception as e:
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def getOrderItems(self, token, user_id, order_id):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": None,
                    "message": "Invalid session",
                    "status": 0
                }
            orderItemsResult = OrderItem.query.filter_by(order_id=order_id).all()
            orderItems = []
            for orderItem in orderItemsResult:
                item = orderItem.item
                orderItems.append({
                    "id": orderItem.id,
                    "item": {
                        "id": item.id,
                        "name": item.name,
                        "bill_name" : item.bill_name,
                    },
                    "qty": orderItem.qty,
                    "is_deleted": orderItem.is_deleted
                })
            return {
                "data": {
                    "orderItems": orderItems,
                },
                "message": "success",
                "status": 1
            }
        except Exception as e:
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def getStocks(self, token, user_id):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": None,
                    "message": "Invalid session",
                    "status": 0
                }
            stocksResult = Stock.query.order_by(Stock.created_date.desc()).all()
            stocks = []
            for stock in stocksResult:
                no_of_items = StockItem.query.filter_by(stock_id=stock.id).count()
                stocks.append({
                    "id": stock.id,
                    "other_details": stock.other_details,
                    "created_date": stock.created_date,
                    "stock_no": stock.stock_no,
                    "no_of_items": no_of_items,
                    "name": stock.user.name
                })
            return {
                "data": {
                    "stocks": stocks,
                },
                "message": "success",
                "status": 1
            }
        except Exception as e:
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def getStockItems(self, token, user_id, stock_id):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": None,
                    "message": "Invalid session",
                    "status": 0
                }
            stockItemsResult = StockItem.query.filter_by(stock_id=stock_id).all()
            stockItems = []
            for stockItem in stockItemsResult:
                item = stockItem.item
                stockItems.append({
                    "id": stockItem.id,
                    "item": {
                        "id": item.id,
                        "name": item.name,
                        "bill_name" : item.bill_name,
                    },
                    "qty": stockItem.qty
                })
            return {
                "data": {
                    "stockItems": stockItems,
                },
                "message": "success",
                "status": 1
            }
        except Exception as e:
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def getRetailers(self, token, user_id):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": None,
                    "message": "Invalid session",
                    "status": 0
                }
            retailersResult = Retailer.query.all()
            retailers = []
            for retailer in retailersResult:
                retailers.append({
                    "id": retailer.id,
                    "name": retailer.name,
                    "address" : retailer.address,
                    "phone_no" : retailer.phone_no,
                    "gstin_no" : retailer.gstin_no,
                })
            return {
                "data": {
                    "retailers": retailers,

                },
                "message": "success",
                "status": 1
            }
        except Exception as e:
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def getItems(self, token, user_id):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": None,
                    "message": "Invalid session",
                    "status": 0
                }
            groupsResult = Group.query.order_by(Group.order).all()
            groups = []
            for group in groupsResult:
                sub_groups = []
                for sub_group in group.sub_groups:
                    items = []
                    for item in sub_group.items:
                        items.append({
                            "id": item.id,
                            "name": item.name,
                            "bill_name": item.bill_name,
                            "available": item.available
                        })
                    sub_groups.append({
                        "id": sub_group.id,
                        "name": sub_group.name,
                        "items": items,
                    })
                groups.append({
                    "id": group.id,
                    "name": group.name,
                    "sub_groups": sub_groups,
                })
            return {
                "data": {
                    "groups": groups,
                },
                "message": "success",
                "status": 1
            }
        except Exception as e:
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def addGroup(self, token, user_id, name):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": None,
                    "message": "Invalid session",
                    "status": 0
                }
            group = Group(name=name, order=1)
            db.session.add(group)
            db.session.commit()
            return {
                "data": {
                    "id": group.id,
                    "name": group.name,
                },
                "message": "success",
                "status": 1
            }
        except Exception as e:
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def addSubGroup(self, token, user_id, group_id, name):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": None,
                    "message": "Invalid session",
                    "status": 0
                }
            subGroup = SubGroup(name=name, group_id=group_id)
            db.session.add(subGroup)
            db.session.commit()
            return {
                "data": {
                    "id": subGroup.id,
                    "name": subGroup.name
                },
                "message": "success",
                "status": 1
            }
        except Exception as e:
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def addItem(self, token, user_id, sub_group_id, name, bill_name):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": None,
                    "message": "Invalid session",
                    "status": 0
                }
            item = Item(name=name, bill_name=bill_name, available=0, ordered=0, sold=0, misc=0, sub_group_id=sub_group_id)
            db.session.add(item)
            db.session.commit()
            return {
                "data": {
                    "id": item.id,
                    "name": item.name,
                    "bill_name": item.bill_name,
                },
                "message": "success",
                "status": 1
            }
        except Exception as e:
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }
# for group in groups:
#     dbGroup = None
#     if group.id is not None:
#         dbGroup = Group.query.filter_by(id=group.id).first()
#     else:
#         dbGroup = Group(name=group.name, order=1)
#         db.session.add(dbGroup)
#     for subGroup in group.sub_groups:
#         dbSubGroup = None
#         if subGroup.id is not None:
#             dbSubGroup = SubGroup.query.filter_by(id=subGroup.id).first()
#         else:
#             dbSubGroup = SubGroup(name=subGroup.name, group=dbGroup)
#             db.session.add(dbSubGroup)
#         for item in subGroup.items:
#             dbItem = Item(name=item.name, bill_name=item.bill_name, available=0, ordered=0, sold=0, misc=0, sub_group=dbSubGroup)
#             db.session.add(dbItem)

    def addRetailer(self, token, user_id, name, address, phone_no, gstin_no):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": None,
                    "message": "Invalid session",
                    "status": 0
                }
            retailer = Retailer(name=name, address=address, phone_no=phone_no, gstin_no=gstin_no)
            db.session.add(retailer)
            db.session.commit()
            return {
                "data": {
                    "retailer": {
                        "id": retailer.id,
                        "name": retailer.name,
                        "address": retailer.address,
                        "phone_no": retailer.phone_no,
                        "gstin_no": retailer.gstin_no,
                    }
                },
                "message": "Retailer added",
                "status": 1
            }
        except Exception as e:
            db.session.rollback()
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def updateRetailer(self, token, user_id, retailer_id, name, address, phone_no, gstin_no):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                return {
                    "data": None,
                    "message": "Invalid session",
                    "status": 0
                }
            retailer = Retailer.query.filter_by(id=retailer_id).first()
            if retailer is None:
                return {
                    "data": None,
                    "message": "Invalid retailer",
                    "status": 0
                }
            retailer.name = name
            retailer.address = address
            retailer.phone_no = phone_no
            retailer.gstin_no = gstin_no
            db.session.commit()
            return {
                "data": {
                    "retailer": {
                        "id": retailer.id,
                        "name": retailer.name,
                        "address": retailer.address,
                        "phone_no": retailer.phone_no,
                        "gstin_no": retailer.gstin_no,
                    }
                },
                "message": "Retailer updated",
                "status": 1
            }
        except Exception as e:
            db.session.rollback()
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def addStock(self, token, user_id, other_details, items):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                raise Exception('Invalid session')
            stockPointer = Pointer.query.filter_by(key="STOCK_NO").first()
            stockPointer.value = stockPointer.value + 1
            stock_no = Utils.getStockNo(stockPointer.value)
            stock = Stock(other_details=other_details, stock_no=stock_no, user_id=user_id) # 1 -> CREATED
            db.session.add(stock)
            items_new = {}
            for item in items:
                if not item["item_id"] in items_new:
                    items_new[item["item_id"]] = item["qty"]
                else:
                    items_new[item["item_id"]] = items_new[item["item_id"]] + item["qty"]
            for id, qty in items_new.items():
                item_db = Item.query.filter_by(id=id).first()
                if item_db is None:
                    raise Exception('Invalid item id')
                stock_item = StockItem(qty=qty, stock=stock, item=item_db)
                db.session.add(stock_item)
                item_db.available = item_db.available + qty
            db.session.commit()
            return {
                "data": {
                    "stock_id": stock.id,
                },
                "message": "Order added",
                "status": 1
            }
        except Exception as e:
            db.session.rollback()
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def addOrder(self, token, user_id, retailer_id, other_details, items):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                raise Exception('Invalid session')
            retailer = Retailer.query.filter_by(id=retailer_id).first()
            if retailer is None:
                raise Exception('Invalid retailer')
            orderPointer = Pointer.query.filter_by(key="ORDER_NO").first()
            orderPointer.value = orderPointer.value + 1
            order_no = Utils.getOrderNo(orderPointer.value)
            order = Order(status=1, other_details=other_details, retailer_id=retailer_id, order_no=order_no) # 1 -> CREATED
            db.session.add(order)
            order_log = OrderLog(date=datetime.datetime.now(), order=order, action=1, user_id=user_id) # 1 -> CREATE_ORDER
            db.session.add(order_log)
            items_new = {}
            for item in items:
                if not item["item_id"] in items_new:
                    items_new[item["item_id"]] = item["qty"]
                else:
                    items_new[item["item_id"]] = items_new[item["item_id"]] + item["qty"]
            for id, qty in items_new.items():
                item_db = Item.query.filter_by(id=id).first()
                if item_db is None:
                    raise Exception('Invalid item id')
                if qty > item_db.available:
                    raise Exception('Invalid order: Quantity more than available!')
                order_item = OrderItem(qty=qty, is_deleted=False, order=order, item=item_db)
                db.session.add(order_item)
                item_db.available = item_db.available - qty
                item_db.ordered = item_db.ordered + qty
            db.session.commit()
            return {
                "data": {
                    "order_id": order.id,
                },
                "message": "Order added",
                "status": 1
            }
        except Exception as e:
            db.session.rollback()
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def updateOrder(self, token, user_id, order_id, retailer_id, other_details, items): # item in list should be unique
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                raise Exception('Invalid session')
            retailer = Retailer.query.filter_by(id=retailer_id).first()
            if retailer is None:
                raise Exception('Invalid retailer')
            order = Order.query.filter_by(id=order_id).first()
            if order is None:
                raise Exception('Invalid order')
            order.status = 2 # EDITED
            order.other_details = other_details
            order.retailer_id = retailer_id
            order_log = OrderLog(date=datetime.datetime.now(), order_id=order_id, action=2, user_id=user_id) # 2 -> EDIT_ORDER
            db.session.add(order_log)
            order_items = OrderItem.query.filter_by(order_id=order_id, is_deleted=False).all()
            items_new = {}
            for item in items:
                if not item["item_id"] in items_new:
                    items_new[item["item_id"]] = {
                        "qty": item["qty"],
                        "isAdded": False
                    }
                else:
                    items_new[item["item_id"]]["qty"] = items_new[item["item_id"]]["qty"] + item["qty"]
            for order_item in order_items:
                if order_item.item_id in items_new:
                    qty = items_new[order_item.item_id]["qty"]
                    if order_item.qty != qty:
                        order_item.is_deleted = True
                        item_db = Item.query.filter_by(id=order_item.item_id).first()
                        if item_db is None:
                            raise Exception('Invalid item id')
                        item_db.available = item_db.available + order_item.qty
                        item_db.ordered = item_db.ordered - order_item.qty
                        if qty > item_db.available:
                            raise Exception('Invalid order: Quantity more than available!')
                        order_item_new = OrderItem(qty=qty, is_deleted=False, order_id=order_id, item=item_db)
                        db.session.add(order_item_new)
                        item_db.available = item_db.available - qty
                        item_db.ordered = item_db.ordered + qty
                    items_new[order_item.item_id]["isAdded"] = True
                else:
                    order_item.is_deleted = True
                    item_db = Item.query.filter_by(id=order_item.item_id).first()
                    if item_db is None:
                        raise Exception('Invalid item id')
                    item_db.available = item_db.available + order_item.qty
                    item_db.ordered = item_db.ordered - order_item.qty
            for id, item in items_new.items():
                if not item["isAdded"]:
                    qty = item["qty"]
                    item_db = Item.query.filter_by(id=id).first()
                    if item_db is None:
                        raise Exception('Invalid item id')
                    if item["qty"] > item_db.available:
                        raise Exception('Invalid order: Quantity more than available!')
                    order_item = OrderItem(qty=item["qty"], is_deleted=False, order=order, item=item_db)
                    db.session.add(order_item)
                    item_db.available = item_db.available - item["qty"]
                    item_db.ordered = item_db.ordered + item["qty"]
            db.session.commit()
            return {
                "data": {
                    "order_id": order.id,
                },
                "message": "Order updated",
                "status": 1
            }
        except Exception as e:
            db.session.rollback()
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    def updateOrderStatus(self, token, user_id, order_id, status):
        try:
            user_session = UserSession.query.filter_by(token=token, user_id=user_id).order_by(UserSession.date.desc()).first()
            if user_session is None or user_session.isDeleted:
                raise Exception('Invalid session')
            if status < 3 or status > 6:
                raise Exception('Invalid status')
            order = Order.query.filter_by(id=order_id).first()
            if order is None:
                raise Exception('Invalid order')
            if status is 4 or status is 6:
                order_items = OrderItem.query.filter_by(order_id=order_id, is_deleted=False).all()
                for order_item in order_items:
                    item_db = Item.query.filter_by(id=order_item.item_id).first()
                    if item_db is None:
                        raise Exception('Invalid item id')
                    if status is 6:
                        order_item.is_deleted = True
                        item_db.available = item_db.available + order_item.qty
                        item_db.ordered = item_db.ordered - order_item.qty
                    if status is 4:
                        item_db.sold = item_db.sold + order_item.qty
                        item_db.ordered = item_db.ordered - order_item.qty
            order.status = status
            order_log = OrderLog(date=datetime.datetime.now(), order_id=order_id, action=status, user_id=user_id)
            db.session.add(order_log)
            db.session.commit()
            return {
                "data": {
                    "order_id": order.id,
                },
                "message": "Order status updated",
                "status": 1
            }
        except Exception as e:
            db.session.rollback()
            return {
                "data": None,
                "message": str(e),
                "status": 0
            }

    # def setBN(self):
    #     groupsResult = Group.query.order_by(Group.order).all()
    #     for group in groupsResult:
    #         for sub_group in group.sub_groups:
    #             for item in sub_group.items:
    #                 item.bill_name = sub_group.name + " " + item.name
    #     db.session.commit()

class Utils:
    @staticmethod
    def getOrderNo(order_no):
        return "OM" + datetime.datetime.now().strftime('%y%m%d') + f'{order_no:04}'

    @staticmethod
    def getStockNo(stock_no):
        return "OS" + datetime.datetime.now().strftime('%y%m%d') + f'{stock_no:04}'


controlManager = ControlManager()

login_json_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['name', 'password']
}

add_user_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'password': {'type': 'string'},
        'email': {'type': 'string'},
        'user_type': {'type': 'number'}
    },
    'required': ['name', 'password', 'email', 'user_type']
}

update_user_type_schema = {
    'type': 'object',
    'properties': {
        'update_user_id': {'type': 'number'},
        'user_type': {'type': 'number'}
    },
    'required': ['update_user_id', 'user_type']
}
# token_schema = {
#     'type': 'object',
#     'properties': {
#         'token': {'type': 'string'},
#         'user_id': {'type': 'number'}
#     },
#     'required': ['token', 'user_id']
# }

retailer_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'address': {'type': 'string'},
        'phone_no': {'type': 'string'},
        'gstin_no': {'type': 'string'},
    },
    'required': ['name', 'address', 'phone_no', 'gstin_no']
}

retailer_update_schema = {
    'type': 'object',
    'properties': {
        'retailer_id': {'type': 'number'},
        'name': {'type': 'string'},
        'address': {'type': 'string'},
        'phone_no': {'type': 'string'},
        'gstin_no': {'type': 'string'},
    },
    'required': ['retailer_id', 'name', 'address', 'phone_no', 'gstin_no']
}

order_schema = {
    'type': 'object',
    'properties': {
        'retailer_id': {'type': 'number'},
        'other_details': {'type': 'string'},
        'items': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'item_id': {'type': 'number'},
                    'qty': {'type': 'number'},
                },
                'required': ['item_id', 'qty']
            }
        },
    },
    'required': ['retailer_id', 'other_details', 'items']
}

stock_schema = {
    'type': 'object',
    'properties': {
        'other_details': {'type': 'string'},
        'items': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'item_id': {'type': 'number'},
                    'qty': {'type': 'number'},
                },
                'required': ['item_id', 'qty']
            }
        },
    },
    'required': ['other_details', 'items']
}

order_upate_schema = {
    'type': 'object',
    'properties': {
        'order_id': {'type': 'number'},
        'retailer_id': {'type': 'number'},
        'other_details': {'type': 'string'},
        'items': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'item_id': {'type': 'number'},
                    'qty': {'type': 'number'},
                },
                'required': ['item_id', 'qty']
            }
        },
    },
    'required': ['retailer_id', 'order_id', 'other_details', 'items']
}

order_status_schema = {
    'type': 'object',
    'properties': {
        'order_id': {'type': 'number'},
        'status': {'type': 'number'},
    },
    'required': ['order_id', 'status']
}

add_group_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
    },
    'required': ['name']
}

add_sub_group_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'group_id': {'type': 'number'},
    },
    'required': ['name', 'group_id']
}

add_item_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'sub_group_id': {'type': 'number'},
        'bill_name': {'type': 'string'},
    },
    'required': ['name', 'sub_group_id', 'bill_name']
}

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/api/v1/seller/login', methods=['POST'])
@expects_json(login_json_schema)
def login():
    response=controlManager.login(name=request.json['name'], password=request.json['password'])
    return jsonify(response), 200

@app.route('/api/v1/seller/logout', methods=['POST'])
def logout():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.logout(token=request.headers['token'], user_id=request.headers['user-id'])
    return jsonify(response), 200

@app.route('/api/v1/seller/add_user', methods=['POST'])
@expects_json(add_user_schema)
def addUser():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.addUser(
        token=request.headers['token'],
        user_id=request.headers['user-id'],
        name=request.json['name'],
        password=request.json['password'],
        email=request.json['email'],
        user_type=request.json['user_type']
    )
    return jsonify(response), 200

@app.route('/api/v1/seller/update_user_type', methods=['PUT'])
@expects_json(update_user_type_schema)
def updateUserType():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.updateUserType(
        token=request.headers['token'],
        user_id=request.headers['user-id'],
        update_user_id=request.json['update_user_id'],
        user_type=request.json['user_type']
    )
    return jsonify(response), 200

@app.route('/api/v1/seller/permissions', methods=['GET'])
def permissions():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.permissions(token=request.headers['token'], user_id=request.headers['user-id'])
    return jsonify(response), 200

@app.route('/api/v1/seller/all_users', methods=['GET'])
def users():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.getUsers(token=request.headers['token'], user_id=request.headers['user-id'])
    return jsonify(response), 200

@app.route('/api/v1/seller/orders', methods=['GET'])
def orders():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.getOrders(token=request.headers['token'], user_id=request.headers['user-id'])
    return jsonify(response), 200

@app.route('/api/v1/seller/order_items', methods=['GET'])
def orderItems():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers or not 'order-id' in request.args:
        abort(400)
    response=controlManager.getOrderItems(token=request.headers['token'], user_id=request.headers['user-id'], order_id=request.args['order-id'])
    return jsonify(response), 200

@app.route('/api/v1/seller/stocks', methods=['GET'])
def stocks():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.getStocks(token=request.headers['token'], user_id=request.headers['user-id'])
    return jsonify(response), 200

@app.route('/api/v1/seller/stock_items', methods=['GET'])
def stockItems():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers or not 'stock-id' in request.args:
        abort(400)
    response=controlManager.getStockItems(token=request.headers['token'], user_id=request.headers['user-id'], stock_id=request.args['stock-id'])
    return jsonify(response), 200

@app.route('/api/v1/seller/items', methods=['GET'])
def items():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.getItems(token=request.headers['token'], user_id=request.headers['user-id'])
    return jsonify(response), 200

@app.route('/api/v1/seller/retailers', methods=['GET'])
def retailers():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.getRetailers(token=request.headers['token'], user_id=request.headers['user-id'])
    return jsonify(response), 200

@app.route('/api/v1/seller/retailer', methods=['POST'])
@expects_json(retailer_schema)
def addRetailer():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.addRetailer(
        token=request.headers['token'],
        user_id=request.headers['user-id'],
        name=request.json['name'],
        address=request.json['address'],
        phone_no=request.json['phone_no'],
        gstin_no=request.json['gstin_no'],
    )
    return jsonify(response), 200

@app.route('/api/v1/seller/retailer', methods=['PUT'])
@expects_json(retailer_update_schema)
def updateRetailer():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.updateRetailer(
        token=request.headers['token'],
        user_id=request.headers['user-id'],
        retailer_id=request.json['retailer_id'],
        name=request.json['name'],
        address=request.json['address'],
        phone_no=request.json['phone_no'],
        gstin_no=request.json['gstin_no'],
    )
    return jsonify(response), 200

@app.route('/api/v1/seller/order', methods=['POST'])
@expects_json(order_schema)
def addOrder():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.addOrder(
        token=request.headers['token'],
        user_id=request.headers['user-id'],
        retailer_id=request.json['retailer_id'],
        other_details=request.json['other_details'],
        items=request.json['items'],
    )
    return jsonify(response), 200

@app.route('/api/v1/seller/stock', methods=['POST'])
@expects_json(stock_schema)
def addStock():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.addStock(
        token=request.headers['token'],
        user_id=request.headers['user-id'],
        other_details=request.json['other_details'],
        items=request.json['items'],
    )
    return jsonify(response), 200

@app.route('/api/v1/seller/order', methods=['PUT'])
@expects_json(order_upate_schema)
def updateOrder():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.updateOrder(
        token=request.headers['token'],
        user_id=request.headers['user-id'],
        order_id=request.json['order_id'],
        retailer_id=request.json['retailer_id'],
        other_details=request.json['other_details'],
        items=request.json['items'],
    )
    return jsonify(response), 200

@app.route('/api/v1/seller/order_status', methods=['PUT'])
@expects_json(order_status_schema)
def updateOrderStatus():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.updateOrderStatus(
        token=request.headers['token'],
        user_id=request.headers['user-id'],
        order_id=request.json['order_id'],
        status=request.json['status'],
    )
    return jsonify(response), 200

@app.route('/api/v1/seller/add_group', methods=['POST'])
@expects_json(add_group_schema)
def addGroup():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.addGroup(
        token=request.headers['token'],
        user_id=request.headers['user-id'],
        name=request.json['name'],
    )
    return jsonify(response), 200

@app.route('/api/v1/seller/add_sub_group', methods=['POST'])
@expects_json(add_sub_group_schema)
def addSubGroup():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.addSubGroup(
        token=request.headers['token'],
        user_id=request.headers['user-id'],
        name=request.json['name'],
        group_id=request.json['group_id'],
    )
    return jsonify(response), 200

@app.route('/api/v1/seller/add_item', methods=['POST'])
@expects_json(add_item_schema)
def addItem():
    if not request.headers or not 'token' in request.headers or not 'user-id' in request.headers:
        abort(400)
    response=controlManager.addItem(
        token=request.headers['token'],
        user_id=request.headers['user-id'],
        name=request.json['name'],
        bill_name=request.json['bill_name'],
        sub_group_id=request.json['sub_group_id'],
    )
    return jsonify(response), 200



    # if not request.json or not 'name' in request.json or not 'password' in request.json:
    #     abort(400)


