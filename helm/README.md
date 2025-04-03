# Updating the Kafka Topic Template

## Adding A New Topic

Submit a PR after adding the new topic and its configuration to
[values.yaml](kafka-topics/values.yaml). GitHub Actions will generate the
required deployment template on submission.

## Update Topic Configuration or Partitions

Make the required changes in [values.yaml](kafka-topics/values.yaml) and
submit a PR, again a GitHub Action will generate the required deployment
template on submission.

**NB:** Use caution when altering Partition counts on existing topics. A
Topic's Partition count can be increased at need, but cannot be reduced
without deletion and recreation of the Topic itself, losing any historic data
within the Topic.

## REF updates

Changes will be automatically deployed to Stage on PR acceptance, but will
require an app-interface MR updating the targeted $ref for Prod deployment.

# Creating Kafka Connectors Template

## Add New Connector Definition
Add new connector configuration to [values.yaml](kafka-connectors/values.yaml) and then run the `helm` command below to generate an updated template.

## Generate Template

Run following command to generate the OpenShift template to create Kafka Connectors.

```sh
$ helm template ./helm/kafka-connectors -f helm/kafka-connectors/values.yaml > deploys/openshift/kafka-connectors.yaml
```
