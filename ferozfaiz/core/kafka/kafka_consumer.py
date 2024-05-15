from django.conf import settings
from confluent_kafka import Consumer, KafkaError
from retrying import retry
import json
import importlib
import logging
import time

logger = logging.getLogger("core")


class KafkaConsumer:
    def __init__(
        self,
        topics,
        group_id,
        server=None,
        auto_offset_reset="earliest",
        commit=False,
    ):
        self.topics = topics
        self.group_id = group_id
        self.server = server or ",".join(settings.KAFKA_SERVERS)
        self.auto_offset_reset = auto_offset_reset
        self.commit = commit
        self.consumer = self.create_consumer()
        self.keep_running = True

    def create_consumer(self):
        return Consumer(
            {
                "bootstrap.servers": self.server,
                "group.id": self.group_id,
                "auto.offset.reset": self.auto_offset_reset,
                "enable.auto.commit": False,
            }
        )

    def subscribe(self):
        self.consumer.subscribe(self.topics)

    def poll_messages(self):
        wait_message_printed = False
        try:
            while self.keep_running:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    if not wait_message_printed:
                        print("No new messages, waiting for tasks...\n")
                        wait_message_printed = True
                    continue
                if msg.error():
                    self.handle_error(msg)
                else:
                    wait_message_printed = False
                    self.process_message(msg)

        finally:
            self.cleanup()

    def handle_error(self, msg):
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print("End of partition reached")
        else:
            raise KafkaError(msg.error())

    def process_message(self, msg):
        data = json.loads(msg.value().decode("utf-8"))
        func_path = data["function"]
        args = data["args"]
        kwargs = data["kwargs"]
        self.execute_task(func_path, *args, **kwargs)

        if self.commit:
            self.consumer.commit(msg, asynchronous=False)

    def execute_task(self, func_path, *args, **kwargs):
        module_name, func_name = func_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        try:
            print(f"Processing task: {func_path}")
            log_message = func_name
            log_message = self.retry_task(
                func, *args, **kwargs, log_message=log_message
            )
            print(log_message)
            print(f"Successfully processed task: {func_path}\n")
        except Exception as e:
            print(f"Error processing task {func_path}: {e}")

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def retry_task(self, func, *args, log_message="", **kwargs):
        start_time = time.time()
        result = func.__wrapped__(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        if result is not None:
            log_message += f" returned {result}"

        # Always output the execution time
        log_message += f" in {execution_time:.15f} seconds."
        return log_message

    def cleanup(self):
        self.keep_running = False
        self.consumer.close()
        print("Kafka consumer stopped gracefully")
