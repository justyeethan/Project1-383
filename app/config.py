import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SESSION_PERMENENT = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'base-secret-key-for-dev'
    SESSION_TYPE = 'filesystem'
    FLASK_ENV = 'development'
