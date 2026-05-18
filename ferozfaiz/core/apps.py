from elasticsearch_dsl import connections
from elasticsearch.transport import Transport
from django.apps import AppConfig
from django.conf import settings
import sys


class HeaderInjectingTransport(Transport):
    def perform_request(self, method, url, headers=None, body=None,  *args, **kwargs):
        if headers is None:
            headers = {}

        headers['CF-Access-Client-Id'] = settings.ELASTICSEARCH_CLIENT_ID
        headers['CF-Access-Client-Secret'] = settings.ELASTICSEARCH_CLIENT_SECRET

        return super(HeaderInjectingTransport, self).perform_request(
            method, url, headers=headers, body=body, *args, **kwargs)


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        if self._should_skip_elasticsearch_init():
            return

        # Use the header-injecting transport class for Elasticsearch connection
        connections.create_connection(
            hosts=self._elasticsearch_hosts(),
            transport_class=HeaderInjectingTransport
        )

        try:
            from core.documents import DjangoLogRecord
            DjangoLogRecord.init()
        except Exception as exc:
            print(f"Elasticsearch index initialization skipped: {exc}", flush=True)

    def _should_skip_elasticsearch_init(self):
        disabled = not getattr(settings, "ELASTICSEARCH_INIT_ON_STARTUP", True)
        management_commands = {"check", "collectstatic", "makemigrations", "migrate", "test"}

        return (
            disabled
            or not self._elasticsearch_hosts()
            or not settings.ELASTICSEARCH_CLIENT_ID
            or not settings.ELASTICSEARCH_CLIENT_SECRET
            or any(command in sys.argv for command in management_commands)
        )

    def _elasticsearch_hosts(self):
        return [
            host for host in [
                settings.ELASTICSEARCH_SERVER_1,
                settings.ELASTICSEARCH_SERVER_2,
            ] if host
        ]
