
from flask_sqlalchemy import SQLAlchemy



# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#     username="MVOFFICEMATE",
#     password="STQ-n6t-ZGq-fKH",
#     hostname="MVOFFICEMATE.mysql.pythonanywhere-services.com",
#     databasename="MVOFFICEMATE$Stationery",
# )

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="",
    hostname="localhost:3306",
    databasename="Stationery",
)

db = None

def initDB(app):
    global db
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)