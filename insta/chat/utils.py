from elasticsearch_dsl import Date,Document,Text,Integer
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections
from . import models

connections.create_connection()

class MessageIndex(Document):
    id = Integer()
    author=Integer()
    content=Text()
    timestamp=Date()

    class Index:
        name='Message-index'

def bulk_index():
    MessageIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Message.objects.all().iterator()))
