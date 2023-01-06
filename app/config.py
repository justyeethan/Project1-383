import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'base-secret-key-for-dev'
    FLASK_ENV = 'development'
