import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'strong_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_DATA', 'sqlite:///data.db' )

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

config = {
    'devconfig' : DevConfig,
    'testconfig' : TestingConfig
}