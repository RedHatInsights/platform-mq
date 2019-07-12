import jinja2
import json
import subprocess
import argparse
import sys
from tempfile import NamedTemporaryFile


DESCRIPTION = 'Create expected topics on a Strimzi Kafka cluster'
TEMPLATE_FILE = "./topictemplate.yaml"
TOPIC_JSON = "./topics.json"
DEV_PROJS = ['platform-mq-dev', 'platform-mq-ci', 'platform-mq-qa']
PROD_PROJS = ['platform-mq-prod']

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('-e', '--environment', help='prod/dev environment for topic creation')
parser.add_argument('-d', '--dryrun', action='store_true',
                    help='Print topics to be created without applying them')
parser.add_argument('-n', '--namespace', help='Specific OpenShift namespace/project for topic creation. Ignores --environment if set')
args = parser.parse_args()

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template(TEMPLATE_FILE)

with open(TOPIC_JSON) as f:
    topics = json.load(f)

if args.environment:
    if args.environment == 'prod':
        namespaces = PROD_PROJS
    else:
        namespaces = DEV_PROJS
elif args.namespace:
    namespaces = [args.namespace]
else:
    sys.exit("--namespace or --environment required")

for ns in namespaces:
    print(ns + '\n')
    CONFIG = {
        "KAFKA_CLUSTER": ns,
        "NAMESPACE": ns
    }

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
                subprocess.call(['oc', 'apply', '-n', ns, '-f', tmpl.name])
