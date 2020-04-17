import yaml
import os

def readConfig(path):
    """
    KafkaConsumer:
      config:
        bootstrap.servers: kafka:9092
        group.id: '0'
      topics:
        - upstream1
        - upstream2
      batchSize: 1
    KafkaProducer:
      config:
        bootstrap.servers: kafka:9092
      topic: downstream1
    AppDatabase:
      connection:
        postgres_host: db
        postgres_port: 5432
        postgres_user: postgres
        postgres_password: password
        postgres_db_name: postgres
        postgres_sslmode: disable
        postgres_sslrootcert:
    """
    config = None
    with open(path, "r") as stream:
        config = yaml.safe_load(stream)
    if config is not None:
        # overrides
        env = os.environ
        if env.get('POSTGRES_PASSWORD'):
            config['AppDatabase']['connection'] = env.get('POSTGRES_PASSWORD')
        if env.get('KAFKA_CONSUMER_SASL_USERNAME'):
            config['KafkaConsumer']['config']['sasl.username'] = env.get('KAFKA_CONSUMER_SASL_USERNAME')
        if env.get('KAFKA_CONSUMER_SASL_PASSWORD'):
            config['KafkaConsumer']['config']['sasl.password'] = env.get('KAFKA_CONSUMER_SASL_PASSWORD')
        if env.get('KAFKA_PRODUCER_SASL_USERNAME'):
            config['KafkaProducer']['config']['sasl.username'] = env.get('KAFKA_PRODUCER_SASL_USERNAME')
        if env.get('KAFKA_PRODUCER_SASL_PASSWORD'):
            config['KafkaProducer']['config']['sasl.password'] = env.get('KAFKA_PRODUCER_SASL_PASSWORD')

        return config
    else:
        return None
