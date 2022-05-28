import os

class Config:
    SECRET_KEY = os.environ.get('strong_key' , 'SECRET_KEY')

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('sqlite:///data.db' , 'FLASK_DATA')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

config = {
    'devconfig' : DevConfig,
    'testconfig' : TestingConfig
}