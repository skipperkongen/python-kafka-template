import logging
from time import sleep
import threading

from confluent_kafka import Consumer, Producer, KafkaException, KafkaError

from my_application.core.models import Action
from my_application.core.db import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kafka')

class KafkaProcessor:

    def __init__(self):
        self.app = None

    def run(self):
        while 1:
            try:
                item = Session.query(Action).first()
                logger.info(f'Tick: {item} from {self}')
                Session.remove()
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
