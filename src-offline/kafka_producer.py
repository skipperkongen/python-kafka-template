import logging
import signal
import time
import os
import random

from confluent_kafka import Producer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kafka_producer')

def handler_stop_signals(signum, frame):
    logger.info('Received SIGTERM/SIGINT, closing program')
    sys.exit()

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

logger.info('Creating producer')

server = os.environ.get('KAFKA_SERVER') or 'kafka:9092'
topic = os.environ.get('KAFKA_TOPIC') or 'alerts'
msg = os.environ.get('KAFKA_MESSAGE') or '{"test":"test"}'
sleep_seconds = int(os.environ.get('SLEEP_SECONDS') or 5)
crap_probability = float(os.environ.get('CRAP_PROPABILITY') or 0.0)
crap_msg = os.environ.get('CRAP_MESSAGE') or '12345abcd$%#@'

producer = Producer({
        'bootstrap.servers': server
})

while True:
    if random.random() < crap_probability:
        send_msg = crap_msg
    else:
        send_msg = msg
    logger.info(f'Producing message: {send_msg}')
    producer.produce(
        topic=topic,
        value=send_msg.encode('utf-8')
    )
    producer.poll(0)
    time.sleep(sleep_seconds)
