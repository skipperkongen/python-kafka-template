import json
import logging
import threading

from confluent_kafka import KafkaException, KafkaError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('core')


class Action:
    def __init__(self, action_type):
        self.action_type = action_type


class Api:

    def __init__(self, engine=None):
        self.lock = threading.Lock()
        self.engine = engine
        self.counter = 0

    def incr(self):
        self.lock.acquire()
        self.counter += 1
        self.lock.release()

    def store_rule(self, rule):
        pass

    def delete_rule(self, rule_id):
        pass

    def disable_rule(self, rule_id):
        pass

    def get_rules(self, group_id=None):
        pass

    def get_actions(self, event):
        yield Action(action_type = 'POST_HTTP')


class ActionExecutor:

    def __init__(self, queue, producer, api):
        self.queue = queue
        self.producer = producer
        self.api = api
        self.topic = 'actions'

    def run(self):
        while 1:
            try:
                action = self.queue.get()
                if action.action_type == 'SEND_EMAIL':
                    self.send_email(action)
                elif action.action_type == 'SEND_SMS':
                    self.send_sms(action)
                elif action.action_type == 'POST_HTTP':
                    self.post_http(action)
                else:
                    raise NotImplementedError(f'Action type not supported: {action.action_type}')
            except Exception as e:
                logger.warning(f'An error occured while executing action: {e}')
            try:
                self.produce(action)
            except Exception as e:
                logger.warning(f'An error occured while producing message: {e}')

        logger.info('Action executor thread terminating!')

    def send_email(self, action):
        raise NotImplementedError(f'Send email not implemented')

    def send_sms(self, action):
        raise NotImplementedError(f'Send SMS not implemented')

    def post_http(self, action):
        raise NotImplementedError(f'Post HTTP not implemented')

    def produce(self, action):
        message = json.dumps(action.__dict__)
        logger.info(f'Producing message: {message}')
        self.producer.produce(
            topic=self.topic,
            value=message.encode('utf-8')
        )
        self.producer.poll(0)

class EventConsumer:

    def __init__(self, queue, consumer, api, database=None, batch_size=5, timeout=10):
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

    def process_event(self, evt):
        logger.info(f'Processing event: {evt}')
        self.api.incr()
        for action in self.api.get_actions(evt):
            self.queue.put(action)


class ParseError(Exception):
    pass
