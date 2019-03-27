
from flask_sqlalchemy import SQLAlchemy



SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Murugappan",
    password="STQ-n6t-ZGq-fKH",
    hostname="Murugappan.mysql.pythonanywhere-services.com",
    databasename="Murugappan$Stationery",
)

db = None

def initDB(app):
    global db
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)