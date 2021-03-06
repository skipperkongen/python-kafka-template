import logging
import json
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
                            for item in self.process_event(evt):
                                self.produce(item)
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
            # logger.info(f'Parsing message: {message}')
            return json.loads(message)
        except:
            raise IgnorableError(message)

    def process_event(self, event):
        # logger.info(f'Processing event: {event}')
        subject = event.get('subject')
        if subject is not None:
            items = Session.query(Action).filter(Action.subject == subject).all()
            for item in items:
                yield item.serialize()
            Session.remove()

    def produce(self, item):
        message = json.dumps(item)
        logger.info(f'Producing message: {message}')
        self.producer.produce(
            topic=self.topic,
            value=message.encode('utf-8')
        )
        self.producer.poll(0)


def create_kafka(config):
    logger.info('Creating Kafka consumer')
    consumer = Consumer(config['kafka']['consumer']['config'])
    consumer_topics = config['kafka']['consumer']['topics']
    for topic in consumer_topics:
        logger.info(f'- {topic}')
    consumer.subscribe(consumer_topics)

    logger.info('Creating Kafka producer')
    producer = Producer(config['kafka']['producer']['config'])
    topic = config['kafka']['producer']['topic']
    kafka = KafkaProcessor(consumer=consumer,
                           producer=producer,
                           topic=topic,
                           batch_size = config['kafka']['consumer']['batch_size'])

    return threading.Thread(target=kafka.run)
