
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from models.base import initDB
from contollers.HelloWorld import hello_world

app = Flask(__name__)

app.config["DEBUG"] = True

initDB(app)

app.register_blueprint(hello_world, url_prefix='/')