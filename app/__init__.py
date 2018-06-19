# third-party imports
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config
import decimal
import flask.json
from flask_cors import CORS

class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.json_encoder = MyJSONEncoder
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    from app import models

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
