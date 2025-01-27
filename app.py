from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)

ma = Marshmallow(app)

@app.route('/')
def welcome():
   return "Hello World!"

from controller import *