import json
import logging
import threading

from confluent_kafka import KafkaException, KafkaError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('core')


class Task:
    def __init__(self, input):
        self.input = input


class Result:
    def __init__(self, input, output):
        self.input = input
        self.output = output


class Api:

    def __init__(self):
        self.lock = threading.Lock()
        self.counter = 0

    def incr(self):
        self.lock.acquire()
        self.counter += 1
        self.lock.release()

    def get_tasks(self, event):
        yield Task('answer_to_everything')


class TaskHandler:

    def __init__(self, queue, api, producer, topic):
        self.queue = queue
        self.producer = producer
        self.api = api
        self.topic = topic

    def run(self):
        while 1:
            try:
                task = self.queue.get()
                result = self.handle_task(task)
            except Exception as e:
                logger.warning(f'An error occured while handling task: {e}')
            try:
                self.produce(result)
            except Exception as e:
                logger.warning(f'An error occured while producing message: {e}')

        logger.info('Action executor thread terminating!')

    def handle_task(self, task):
        return Result(task.input, 42)

    def produce(self, result):
        message = json.dumps(result.__dict__)
        logger.info(f'Producing message: {message}')
        self.producer.produce(
            topic=self.topic,
            value=message.encode('utf-8')
        )
        self.producer.poll(0)


class EventConsumer:

    def __init__(self, queue, consumer, api, database=None, batch_size=5, timeout=5):
        self.queue = queue
        self.consumer = consumer
        self.api = api
        self.database = database
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
                    except (ParseError) as e:
                        logger.warning(f'Ignoring {type(e).__name__} {e}')
                        self.consumer.commit(msg)
                    except Exception as e:
                        logger.error(f'Not ignoring {type(e).__name__} {e}')
            except (Exception):
                logger.exception(e)
        logger.info('Event consumer thread terminating!')

    def parse_message(self, message):
        try:
            # JSON or bust!!
            return json.loads(message)
        except:
            raise ParseError(message)

    def process_event(self, event):
        logger.info(f'Processing event: {event}')
        self.api.incr()
        for task in self.api.get_tasks(event):
            self.queue.put(task)


class ParseError(Exception):
    pass
