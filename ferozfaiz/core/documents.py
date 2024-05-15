from elasticsearch_dsl import Document, Date, Text, Integer, connections

# Define a default Elasticsearch client
# connections.create_connection(hosts=['localhost'])


class DjangoLogRecord(Document):
    levelname = Text()
    asctime = Date()
    module = Text()
    message = Text()
    pathname = Text()
    lineno = Integer()
    funcName = Text()

    class Index:
        # Name of the Elasticsearch index
        name = 'django-log-records'


# Create the index in Elasticsearch if it doesn't exist
# DjangoLogRecord.init()
