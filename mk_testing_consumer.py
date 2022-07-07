from kafka import KafkaConsumer
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import ssl
import argparse

parser = argparse.ArgumentParser()
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
    ssl_context=ssl.create_default_context(),
    enable_auto_commit=True,
    )

consumer.subscribe(topics=args.topics)
while True:
    msgs = consumer.poll()
    if msgs:
        print(msgs)
