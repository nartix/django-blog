from django.core.management.base import BaseCommand
from core.kafka import KafkaConsumer
import signal


# python manage.py startkafkaconsumer mytopic mytopic-group --commit
# --auto-offset-reset=earliest


class Command(BaseCommand):
    help = "Starts the Kafka consumer for processing tasks"

    def add_arguments(self, parser):
        parser.add_argument("topic", type=str, help="The Kafka topic to subscribe to")
        parser.add_argument("group_id", type=str, help="The consumer group ID")
        parser.add_argument(
            "--commit", action="store_true", help="Commit offsets to Kafka"
        )
        parser.add_argument(
            "--auto-offset-reset",
            type=str,
            default="earliest",
            choices=["earliest", "latest"],
            help="Set the offset reset policy",
        )

    def handle(self, *args, **options):
        topic = options["topic"]
        group_id = options["group_id"]
        commit = options["commit"]
        auto_offset_reset = options["auto_offset_reset"]

        consumer = KafkaConsumer(
            topics=[topic],
            group_id=group_id,
            auto_offset_reset=auto_offset_reset,
            commit=commit,
        )

        signal.signal(signal.SIGINT, self.signal_handler(consumer))
        signal.signal(signal.SIGTERM, self.signal_handler(consumer))

        self.stdout.write(
            self.style.SUCCESS(
                f'Kafka consumer for topic "{topic}" in group "{group_id}" started ...'
            )
        )

        consumer.subscribe()
        consumer.poll_messages()

    def signal_handler(self, consumer):
        def handle_signal(signal_received, frame):
            self.stdout.write(
                self.style.WARNING("\nSignal received, initiating graceful shutdown...")
            )
            consumer.keep_running = False

        return handle_signal
