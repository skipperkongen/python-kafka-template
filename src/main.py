from configurator import Config
import signal

from my_application.web import create_app
from my_application.kafka import create_kafka

def handler_stop_signals(signum, frame):
    logger.info('Received SIGTERM/SIGINT, closing program')

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

config = Config.from_path('/app/config.yaml', optional=True)

app = create_app(config)
kafka = create_kafka(config)
kafka.start()
