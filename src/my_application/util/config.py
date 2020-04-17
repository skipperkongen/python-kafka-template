import yaml
import os

def readConfig(path='/app/config.yaml' ):
    config = None
    with open(path, "r") as stream:
        config = yaml.safe_load(stream)
    if config is not None:
        # overrides
        env = os.environ
        if env.get('DATABASE_CONNECTION'):
            config['database']['connection'] = env.get('DATABASE_CONNECTION')
        if env.get('KAFKA_CONSUMER_USERNAME'):
            config['kafka']['consumer']['config']['sasl.username'] = env.get('KAFKA_CONSUMER_USERNAME')
        if env.get('KAFKA_CONSUMER_PASSWORD'):
            config['kafka']['consumer']['config']['sasl.password'] = env.get('KAFKA_CONSUMER_PASSWORD')
        if env.get('KAFKA_PRODUCER_USERNAME'):
            config['kafka']['producer']['config']['sasl.username'] = env.get('KAFKA_PRODUCER_USERNAME')
        if env.get('KAFKA_PRODUCER_PASSWORD'):
            config['kafka']['producer']['config']['sasl.password'] = env.get('KAFKA_PRODUCER_PASSWORD')
        if env.get('FLASK_JWT_SECRET_KEY'):
            config['Flask']['jwt_secret_key'] = env.get('FLASK_JWT_SECRET_KEY')
        if env.get('FLASK_SECRET_KEY'):
            config['Flask']['secret_key'] = env.get('FLASK_SECRET_KEY')
        if env.get('FLASK_USERNAME'):
            config['Flask']['username'] = env.get('FLASK_USERNAME')
        if env.get('FLASK_PASSWORD'):
            config['Flask']['password'] = env.get('FLASK_PASSWORD')
        return config
    else:
        return None

config = readConfig()
