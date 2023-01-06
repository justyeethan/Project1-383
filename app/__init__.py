from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__) # Init the flask app
Bootstrap(app) # Enables Flask bootstrap
app.config.from_object(Config) # Sets config object from config.py
app.debug = True
# Database creation

from app import routes # Initializes all files
