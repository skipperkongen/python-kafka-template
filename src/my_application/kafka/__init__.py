import logging
from time import sleep
import threading

from confluent_kafka import Consumer, Producer, KafkaException, KafkaError

from my_application.web.model import Action

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kafka')

class KafkaProcessor:

    def __init__(self):
        self.app = None

    def run(self):
        while 1:
            try:
                with self.app.app_context():
                    item = Action.query.first()
                logger.info(f'Tick: {item}')
            except Exception as e:
                logger.exception(e)
            finally:
                sleep(5)

    def init_app(self, app):
        self.app = app

def create_kafka(config, app):
    kafka = KafkaProcessor()
    kafka.init_app(app)
    return threading.Thread(target=kafka.run)
