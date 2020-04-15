import logging
import signal

from confluent_kafka import Producer, Consumer
import yaml

from my_application.util.config import readConfig
from my_application.kafka import create_kafka

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')

def handler_stop_signals(signum, frame):
    logger.info('Received SIGTERM/SIGINT, closing program')

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

config = readConfig('/app/config.yaml')

kafka = create_kafka(config)
kafka.start()
