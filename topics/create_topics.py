import jinja2
import json
import subprocess
import argparse
from tempfile import NamedTemporaryFile


DESCRIPTION = 'Create expected topics on a Strimzi Kafka cluster'
TEMPLATE_FILE = "./topictemplate.yaml"
TOPIC_JSON = "./topics.json"

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('namespace', help='OpenShift namespace in which to create the topics.')
parser.add_argument('cluster', help='Strimzi cluster in which to create the topics.')
parser.add_argument('-d', '--dryrun', action='store_true',
                    help='Print topics to be created without applying them')
args = parser.parse_args()

CONFIG = {
    "KAFKA_CLUSTER": args.cluster,
    "NAMESPACE": args.namespace
}

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template(TEMPLATE_FILE)

with open(TOPIC_JSON) as f:
    topics = json.load(f)

for topic in topics:
    if 'TOPIC_CONFIGS' not in topic:
        topic['TOPIC_CONFIGS'] = "{}"
    topic.update(CONFIG)
    rendered = template.render(**topic)
    if args.dryrun:
        print("{}\n\n".format(rendered))
    else:
        with NamedTemporaryFile(dir='.') as tmpl:
            tmpl.write(template.render(**topic))
            tmpl.flush()
            subprocess.call(['oc', 'apply', '-n', args.namespace, '-f', tmpl.name])
