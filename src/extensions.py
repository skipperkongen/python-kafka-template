from flask_bootstrap import Bootstrap
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
jwt_manager = JWTManager()
migrate = Migrate()
db = SQLAlchemy()
