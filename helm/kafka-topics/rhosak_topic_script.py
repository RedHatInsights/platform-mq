import requests
import yaml
import sys
import http
import argparse
import getpass

def get_token(token_url, client_id, client_secret):
    auth = {"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"}
    r = requests.post(token_url, auth)
    r.raise_for_status()
    token = r.json().get('access_token')
    return token

def create_topic(admin_url, topic_name, topic_parts, token, prefix):
    topic_url = f'{admin_url}/api/v1/topics'
    headers = {"Authorization": f"Bearer {token}", "Content-type": "application/json"}
    topic_config = {'name': f'{prefix}.{topic_name}', 'settings': {'numPartitions': topic_parts}}
    r = requests.post(topic_url, json=topic_config, headers=headers)
    if r.status_code == http.HTTPStatus.CONFLICT:
        print(f'Topic: {topic_config} already exists. Skipping.')
        return
    r.raise_for_status()
    print(r.json().get('id'))

def all_topics(admin_url, token, prod):
    with open('./values.yaml') as f:
        topics = yaml.safe_load(f)

    if prod:
        prefix = "platform-mq-prod"
    else:
        prefix = "platform-mq-stage"

    for topic in topics.get('topics'):
        topic_name = topic.get("topic_name")
        topic_parts = topic.get("partitions")
        print(f'{topic_name} -- {topic_parts}')
        create_topic(admin_url, topic_name, topic_parts, token, prefix)

def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token_endpoint", default='https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token')
    parser.add_argument("admin_endpoint")
    parser.add_argument("client_id")
    parser.add_argument("-p", "--prod", action="store_true")
    return parser

def main():
    parser = setup_parser()
    args = parser.parse_args()
    pw = getpass.getpass(prompt=f'client id for {args.client_id}: ')

    token = get_token(args.token_endpoint, args.client_id, pw)
    all_topics(args.admin_endpoint, token, args.prod)

if __name__ == "__main__":
    main()
