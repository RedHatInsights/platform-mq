import jinja2
import json
import subprocess
import argparse
from tempfile import NamedTemporaryFile


DESCRIPTION = 'Create required testing topics on a Strimzi Kafka cluster'
TEMPLATE_FILE = "topictemplate.yaml"
TOPIC_LIST = "./topics.json"

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('namespace', help='OpenShift namespace in which to create the topics.')
parser.add_argument('-c', '--cluster', help='Strimzi cluster in which to create the topics.')
args = parser.parse_args()

CONFIG = {
    "PARTITIONS": 3,
    "REPLICAS": 3,
    "KAFKA_CLUSTER": args.cluster,
    "NAMESPACE": args.namespace
}

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template(TEMPLATE_FILE)

with open(TOPIC_LIST) as f:
    topics = json.load(f)

for topic in topics:
    CONFIG["TOPIC_NAME"] = topic
    with NamedTemporaryFile(dir='.') as tmpl:
        tmpl.write(template.render(**CONFIG))
        tmpl.flush()
        subprocess.call(['oc', 'create', '-n', args.namespace, '-f', tmpl.name])
