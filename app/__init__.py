from flask import Flask
import os
from app.config import Config
from flask_session import Session

app = Flask(__name__) # Init the flask app
app.config.from_object(Config) # Sets config object from config.py
app.debug = True # Debug is live
Session(app) # Sessions Integration

from app import routes # Initializes all files from app DO NOT MOVE TO TOP OF FILE
