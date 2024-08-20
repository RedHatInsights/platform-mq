# Creating Kafka Topic Template

## Install Helm

See [docs](https://helm.sh/docs/) to [install](https://helm.sh/docs/intro/install/) Helm.

## Generate Template

Run following command to generate the OpenShift template to create the Kafka topics.

```sh
$ helm template ./helm/kafka-topics -f helm/kafka-topics/values.yaml > deploys/openshift/kafka-topics.yaml
```

## Add New Topic

Add new topic and its configuration to [values.yaml](kafka-topics/values.yaml) and then run the `helm` command above to generate updated template.

## Update Topic Configuration or Partitions

Make the required changes in [values.yaml](kafka-topics/values.yaml) and then run the `helm` command above to generate an updated template.

## PRs and REF updates

After making any changes that require generating an updated template, make a PR here with the updated template and values.yaml files. Once merged in, the platform-mq ref in App-Interface can be updated to deploy the new changes to stage/prod.


# Creating Kafka Connectors Template

## Add New Connector Definition

Add new connector configuration to [values.yaml](kafka-connectors/values.yaml) and then run the `helm` command below to generate an updated template.

## Generate Template

Run following command to generate the OpenShift template to create Kafka Connectors.

```sh
$ helm template ./helm/kafka-connectors -f helm/kafka-connectors/values.yaml > deploys/openshift/connectors/kafka-connectors.yaml
```
