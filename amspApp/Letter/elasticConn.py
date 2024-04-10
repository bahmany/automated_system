from elasticsearch import Elasticsearch

from amsp import settings
from amsp.settings import ELASTIC_IP_PASSWORD


def getElasticSearch():
    return Elasticsearch("http://" + ELASTIC_IP_PASSWORD,
                         )
