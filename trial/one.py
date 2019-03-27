a = 5

def change():
    global a
    a = 10
    print(a)

def changes(app):
    print(app)
    app["isChanged"] = True

print(a)

from models import User, Retailer, Order, OrderItem, Stock, StockItem, OrderLog, Group, SubGroup, Item, UserSession, Pointer
