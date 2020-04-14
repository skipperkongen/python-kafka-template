from flask_bootstrap import Bootstrap
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

bootstrap = Bootstrap()
jwt_manager = JWTManager()
migrate = Migrate()
