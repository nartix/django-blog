from elasticsearch_dsl import connections
from elasticsearch.transport import Transport
from django.apps import AppConfig
from django.conf import settings


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
        # Use the header-injecting transport class for Elasticsearch connection
        connections.create_connection(
            hosts=[settings.ELASTICSEARCH_SERVER_1,
                   settings.ELASTICSEARCH_SERVER_2],
            transport_class=HeaderInjectingTransport
        )

        # Initialize documents as before
        from core.documents import DjangoLogRecord
        DjangoLogRecord.init()
