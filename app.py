
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from models.base import initDB

app = Flask(__name__)

app.config["DEBUG"] = True

initDB(app)

@app.route('/')
def hello_world():
    return 'I am Flash, I am awesome!'