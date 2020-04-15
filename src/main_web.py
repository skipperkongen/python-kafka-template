import logging
import signal

# from configurator import Config
from flask import Flask, Response

from my_application.web.config import config
from my_application.core.db import Session, engine
from my_application.core.models import Base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')

def handler_stop_signals(signum, frame):
    logger.info('Received SIGTERM/SIGINT, closing program')

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

# config = Config.from_path('/app/config.yaml', optional=True)
config = config


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
#    init_db()

    return app


def register_extensions(app):
    from my_application.web.extensions import bootstrap
    from my_application.web.extensions import jwt_manager

    bootstrap.init_app(app)
    jwt_manager.init_app(app)


    #from my_application.web.extensions import migrate
    #from my_application.web.model import db
    #migrate.init_app(app, db)
    #db.init_app(app)
    #db.create_all(app=app)


def register_blueprints(app):
    from my_application.web.views import auth_bp
    from my_application.web.views import action_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(action_bp)


#def init_db():
#    Base.metadata.create_all(engine)


app = create_app(config)


@app.teardown_appcontext
def teardown_db(resp_or_exc):
    Session.remove()
