import logging
from time import sleep
import threading

from confluent_kafka import Consumer, Producer, KafkaException, KafkaError

from my_application.core.models import Action
from my_application.core.db import Session

class IgnorableError(Exception):
    pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kafka')

class KafkaProcessor:

    def __init__(self, consumer, producer, topic, batch_size=5, timeout=5):
        self.consumer = consumer
        self.producer = producer
        self.topic = topic
        self.batch_size = batch_size
        self.timeout = timeout

    def run(self):
        logger.info('Starting event consumer loop')
        while 1:
            try:
                msgs = self.consumer.consume(
                    num_messages=self.batch_size,
                    timeout=self.timeout
                )
                logger.info(f'Consumed {len(msgs)} messages from Kafka')
                for msg in msgs:
                    try:
                        # Get error. Might be None.
                        kafka_error = msg.error()
                        if kafka_error is not None:
                            # Handle error
                            if kafka_error.fatal():
                                # Fatal error
                                logger.error(f'Kafka fatal error: {kafka_error}')
                                raise KafkaException(msg.error())
                            else:
                                # Non-fatal error
                                logger.info(f'Kafka non-fatal error: {kafka_error.name} at offset {msg.offset()}')
                        else:
                            # Handle message
                            evt = self.parse_message(msg.value())
                            self.process_event(evt)
                        self.consumer.commit(msg)
                    except IgnorableError as e:
                        logger.warning(f'Ignoring error: {e}')
                        self.consumer.commit(msg)
                    except Exception as e:
                        logger.error(f'Not ignoring {type(e).__name__} {e}')
            except Exception as e:
                logger.exception(e)
        logger.info('Event consumer thread terminating!')

    def parse_message(self, message):
        try:
            # JSON or bust!!
            return json.loads(message)
        except:
            raise IgnorableError(message)

    def process_event(self, event):
        logger.info(f'Processing event: {event}')
        # item = Session.query(Action).first()
        # logger.info(f'Tick: {item} from {self}')
        # Session.remove()


def create_kafka(config):
    logger.info('Creating Kafka consumer')
    consumer = Consumer(config['KafkaConsumer']['config'])
    consumer_topics = config['KafkaConsumer']['topics']
    for topic in consumer_topics:
        logger.info(f'- {topic}')
    consumer.subscribe(consumer_topics)

    logger.info('Creating Kafka producer')
    producer = Producer(config['KafkaProducer']['config'])
    topic = config['KafkaProducer']['topic']
    kafka = KafkaProcessor(consumer=consumer,
                           producer=producer,
                           topic=topic)

    return threading.Thread(target=kafka.run)
