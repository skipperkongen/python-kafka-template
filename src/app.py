import json
import logging
from queue import SimpleQueue
import signal
import threading

#from configurator import Config
from confluent_kafka import Consumer, Producer, KafkaException, KafkaError
from flask import Flask, Response, request, jsonify

from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')

# from app import ParseError, Api, EventConsumer, TaskHandler

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    return app

def register_extensions(app):
    from extensions import bootstrap
    from extensions import db
    from extensions import jwt_manager
    from extensions import migrate

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)


def register_blueprints(app):
    from api import api_bp
    from auth import auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

app = create_app()
