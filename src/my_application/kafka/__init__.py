import logging
from time import sleep
import threading

from confluent_kafka import Consumer, Producer, KafkaException, KafkaError


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kafka')

class KafkaProcessor:
    def run(self):
        while 1:
            logger.info('Tick')
            sleep(5)

def create_kafka(config):
    kafka_processor = KafkaProcessor()
    event_consumer_thread = threading.Thread(target=kafka_processor.run)
    return event_consumer_thread
