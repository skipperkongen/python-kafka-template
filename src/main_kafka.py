# from configurator import Config
# config = Config.from_path('/app/config.yaml', optional=True)


# kafka = create_kafka(config, app)
# kafka.start()
import logging
import signal

# from configurator import Config

from my_application.web.config import config
from my_application.core.db import Session, engine
from my_application.core.models import Base


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')

def handler_stop_signals(signum, frame):
    logger.info('Received SIGTERM/SIGINT, closing program')

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)
