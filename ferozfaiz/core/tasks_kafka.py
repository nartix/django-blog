from core.kafka import kafka_task
import logging
from core.documents import DjangoLogRecord

logger = logging.getLogger("test")


@kafka_task('mytopic')
def my_first_kafka_task(num, num2):
    # return num + num2
    pass
    # return True


# DO NOT USE LOGGING IN THIS KAFKA TASKS AS IT WILL PRODUCE INFINITE RECURSION
@kafka_task('djangologs', log=True)
def django_logger_task(log_record):
    # print("Received log record for Kafka: %s", log_record)
    # logger.info("Executing log record Kafka: %s", log_record)
    # return True
    log_doc = DjangoLogRecord(**log_record)
    # Save the document in Elasticsearch
    log_doc.save()
    print("Log record saved in Elasticsearch: %s", log_record)
    return True
