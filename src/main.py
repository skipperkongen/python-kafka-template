import json
import logging
from queue import SimpleQueue
import signal
import threading

from configurator import Config
from confluent_kafka import Consumer, Producer, KafkaException, KafkaError
from flask import Flask, Response, request, jsonify

from pkt import ParseError, Api, EventConsumer, ActionExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')

def handler_stop_signals(signum, frame):
    logger.info('Received SIGTERM/SIGINT, closing program')

signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)

# Load config
logger.info('Reading configuration')
config = Config.from_path('/app/config.yaml', optional=True)


logger.info(f"Initializing API")

api = Api()
action_queue = SimpleQueue()

logger.info(f"Starting action executor thread")
# Create Kafka producers
producer = Producer(dict(config['KafkaProducer']['config'].items()))
action_executor = ActionExecutor(queue=action_queue, producer=producer, api=api)
action_executor_thread = threading.Thread(target=action_executor.run)
action_executor_thread.start()

logger.info(f"Starting event consumer thread")
consumer = Consumer(dict(config['KafkaConsumer']['config'].items()))
consumer_topics = list(config['KafkaConsumer']['topics'])
logger.info(f'Subscribing to topics:')
for topic in consumer_topics:
    logger.info(f'- {topic}')
consumer.subscribe(consumer_topics)
event_consumer = EventConsumer(queue=action_queue, consumer=consumer, api=api)
event_consumer_thread = threading.Thread(target=event_consumer.run)
event_consumer_thread.start()

logger.info('Starting REST interface')
# Create the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dudu-dodo-didi-dada'

@app.route('/', methods=['GET'])
def hello():
    return Response(f'Hello World!', mimetype='text/plain')

logger.info('Ready to receive requests')
