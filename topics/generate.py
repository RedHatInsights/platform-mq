import jinja2
import json
import subprocess
from tempfile import NamedTemporaryFile

CONFIG = {
    "PARTITIONS": 1,
    "REPLICAS": 3,
    "KAFKA_CLUSTER": 'platform-mq'
}

NAMESPACE = 'cmitchel-testing'

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
        subprocess.call(['oc', 'create', '-n', NAMESPACE, '-f', f.name])
