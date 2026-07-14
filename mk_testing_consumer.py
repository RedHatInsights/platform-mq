"""
Example script for connecting to MSK and consuming messages via SASL/SSL.

Demonstrates how to authenticate and consume from Kafka topics using SASL_PLAIN
authentication. Useful for testing MSK connectivity and debugging message flow.

Usage:
    python mk_testing_consumer.py \\
        -b bootstrap.server1:9096,bootstrap.server2:9096 \\
        -u your_sasl_username \\
        -p your_sasl_password \\
        -t topic.name \\
        --from-beginning

Dependencies:
    pip install kafka-python requests-oauthlib

Example:
    # Consume from beginning of topic
    python mk_testing_consumer.py \\
        -b $MSK_BOOTSTRAP_SERVERS \\
        -u $MSK_USER \\
        -p $MSK_PASSWORD \\
        -t platform.notifications.ingress \\
        --from-beginning
"""

from kafka import KafkaConsumer
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import ssl
import argparse
import logging

#logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
opt = parser.add_argument_group('optional')
opt.add_argument('--from-beginning', action='store_true')
reqd = parser.add_argument_group('required arguments')
reqd.add_argument('-b','--bootstrap_servers', nargs='+', required=True)
reqd.add_argument('-u', '--client_id', required=True)
reqd.add_argument('-p', '--client_secret', required=True)
reqd.add_argument('-t', '--topics', nargs='+', required=True)

args = parser.parse_args()

consumer = KafkaConsumer(
    group_id="mk_test_consumer",
    bootstrap_servers=args.bootstrap_servers,
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username = args.client_id,
    sasl_plain_password = args.client_secret,
    ssl_check_hostname=False,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    )

consumer.subscribe(topics=args.topics)
if args.from_beginning:
    consumer.seek_to_beginning()
while True:
    msgs = consumer.poll()
    if msgs:
        print(msgs)
