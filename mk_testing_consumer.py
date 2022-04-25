from kafka import KafkaConsumer
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import ssl
import argparse

token_url = "https://identity.api.openshift.com/auth/realms/rhoas/protocol/openid-connect/token"


class TokenProvider(object):
    def __init__(self, client_id, client_secret, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url

    def token(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token_json = oauth.fetch_token(token_url=token_url, client_id=self.client_id, client_secret=self.client_secret)
        token = token_json['access_token']
        return token


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
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=TokenProvider(args.client_id, args.client_secret, token_url),
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
