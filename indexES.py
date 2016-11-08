from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])
for listing in consumer:
    listingjson = json.loads((listing.value).decode('utf-8'))
    es.index(index='listing_index', doc_type='listing', id=listingjson['id'], body=listing)
    es.indices.refresh(index="listing_index")
