import os
from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError


c = AvroConsumer({
    'bootstrap.servers': os.environ.get('KAFKA_SERVERS'),
    'group.id': 'groupid',
    'schema.registry.url': os.environ.get('SCHEMA_REGISTRY')})

c.subscribe([os.environ.get('TOPIC')])

for i in range(int(os.environ.get('ITERATIONS'))):
    try:
        msg = c.poll(10)

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    print(msg.value())

c.close()
