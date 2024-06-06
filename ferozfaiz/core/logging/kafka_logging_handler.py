from logging import Handler
from core.tasks_kafka import django_logger_task
import logging

logger = logging.getLogger("test")


class KafkaLoggingHandler(Handler):
    def __init__(self):
        super().__init__()
        # self.topic = topic

    def emit(self, record):
        # Skip logs from Elasticsearch DSL
        if record.module in ["_transport", "connectionpool", "elasticsearch", "elasticsearch_dsl"]:
            return

        log_record_dict = {
            "levelname": record.levelname,
            "asctime": self.formatter.formatTime(record),
            "module": record.module,
            "message": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno,
            "funcName": record.funcName,
        }

        logger.info("Log record dictionary: %s", log_record_dict)

        # Send the dictionary to the Kafka task
        # django_logger_task(log_record_dict)
