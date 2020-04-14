import logging

from flask import Flask, Response


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')


def create_app(config):
    app = Flask(__name__)
    from my_application.web.config import config

    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    return app

def register_extensions(app):
    from my_application.web.extensions import bootstrap
    from my_application.web.extensions import jwt_manager
    from my_application.web.extensions import migrate
    from my_application.web.model import db

    db.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)

    db.create_all(app=app)


def register_blueprints(app):
    from my_application.web.views import auth_bp
    from my_application.web.views import action_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(action_bp)
