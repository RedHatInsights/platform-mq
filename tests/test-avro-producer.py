import os
import datetime
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

data = {
    "rh_account": "12345",
    "principal": "myprince",
    "validation": False,
    "size": 1237859,
    "service": "bob",
    "url": "www.dotcom.com"
}

json_schema = os.environ.get('SCHEMA')
parsed_schema = avro.loads(json_schema)

avroProducer = AvroProducer({
    'bootstrap.servers': os.environ.get('KAFKA_SERVERS'),
    'schema.registry.url': os.environ.get('SCHEMA_REGISTRY')},
    default_value_schema=parsed_schema)

for i in range(int(os.environ.get('ITERATIONS'))):
    data['payload_id'] = datetime.datetime.now().strftime('%s')
    print(data)
    avroProducer.produce(topic=os.environ.get('TESTTOPIC'), value=data)
    avroProducer.flush()
