from confluent_kafka import Producer
from django.conf import settings
import json
import functools

import logging

logger = logging.getLogger("test")

# Configuration for Confluent Kafka Producer
config = {
    # 'bootstrap.servers': 'localhost:9092',
    'bootstrap.servers': ','.join(settings.KAFKA_SERVERS),
}

producer = Producer(**config)


def kafka_task(topic, log=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # reference to the original function
            result = func

            # Kafka message production logic
            message = {
                'function': f"{func.__module__}.{func.__name__}",
                'args': args,
                'kwargs': kwargs
            }
            message_bytes = json.dumps(message).encode('utf-8')

            def acked(err, msg):
                if err is not None:
                    print(f"Failed to deliver message: {err}")
                    # Logger must be disabled for LogHandler to prevent infinite loop
                    logger.error(
                        f"Failed to deliver message: {err}") if log else None
                else:
                    print(
                        f"Message delivered to {msg.topic()} [{msg.partition()}]")
                    logger.info(
                        f"Message delivered to {msg.topic()} [{msg.partition()}]") if log else None

            producer.produce(topic, value=message_bytes, callback=acked)
            producer.flush()

            # return the reference so it can be called by __wrapped__ without decorator
            return result
        return wrapper
    return decorator
