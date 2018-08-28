import jinja2
import json
import subprocess
import argparse
from tempfile import NamedTemporaryFile


DESCRIPTION = 'Create required testing topics on a Strimzi Kafka cluster'

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('namespace', help='OpenShift namespace in which to create the topics.')
args = parser.parse_args()

CONFIG = {
    "PARTITIONS": 1,
    "REPLICAS": 3,
    "KAFKA_CLUSTER": 'platform-mq'
}

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.yaml"
template = templateEnv.get_template(TEMPLATE_FILE)

with open('./topics.json') as f:
    topics = json.load(f)

for topic in topics:
    CONFIG["TOPIC_NAME"] = topic
    with NamedTemporaryFile(dir='.') as f:
        f.write(template.render(**CONFIG))
        f.flush()
        subprocess.call(['oc', 'create', '-n', args.namespace, '-f', f.name])
