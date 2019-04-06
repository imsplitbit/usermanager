from flask_api import FlaskAPI

from instance.config import app_config
from usrmgr.models import db
from usrmgr.blueprints.user import users


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(users)

    return app
