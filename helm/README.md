# Creating Kafka Topic Template

## Install Helm

See [docs](https://helm.sh/docs/) to [install](https://helm.sh/docs/intro/install/) Helm.

## Generate Template

Run following command to generate the OpenShift template to create the Kafka topics.

```sh
$ helm template ./helm/kafka-topics -f helm/kafka-topics/values.yaml > deploys/openshift/kafka-topics.yaml
```

## Add New Topic

Add new topic and its configuration to [values.yaml](kafka-topics/values.yaml) and then run `helm` command to generate updated template.
