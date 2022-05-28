from flask import Flask
from config import config

def create_app(app_config):
    app = Flask(__name__)
    app.config.from_object(config[app_config])

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app 