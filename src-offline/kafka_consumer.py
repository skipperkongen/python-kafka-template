import logging
import signal
import time
import os

from confluent_kafka import Consumer, KafkaException, KafkaError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kafka_consumer')

def handler_stop_signals(signum, frame):
    logger.info('Received SIGTERM/SIGINT, closing program')
    sys.exit()

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

server = os.environ.get('KAFKA_SERVER') or 'kafka:9092'
topic = os.environ.get('KAFKA_TOPIC') or 'actions'
consumer_group = os.environ.get('KAFKA_CONSUMER_GROUP') or 'actions'

consumer = Consumer({
        'bootstrap.servers': server,
        'group.id': consumer_group,
        'enable.auto.commit': True
})

consumer.subscribe([topic])

while True:
    msg = consumer.poll(timeout=10.0)
    if msg is None:
        logger.info(f'Nothing received...')
        continue
    if msg.error():
        # Error or event
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition event
            logger.error(f' {msg.topic()} [{msg.partition()}] reached end of offset {msg.offset()}')
        else:
            # Error
            logger.error(f' Fatal error: {msg.error()}')
            raise KafkaException(msg.error())
    else:
        logger.info(f' Message received: {msg.value()}')
