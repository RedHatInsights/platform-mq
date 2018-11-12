# Insights Platform Messaging Service

This Messaging Service is designed to work as the piping between Platform
client services.

## Details

The Messaging Service backs the different components of Insights Platform to
allow for cross-application and intra-application communication. This is
achieved with an OpenShift based deployment of Apache's Kafka message queue as
deployed and orchestrated by the forthcoming AMQ Streams Red Hat project.

Currently we're running the upstream product for AMQ Streams, Strimzi, at
version 0.7.0.

The service runs entirely in Openshift Dedicated.

## How it Works

The Messaging Service is a standard deployment of Apache Kafka orchestrated by
Strimzi. Product documentation is available at:

http://strimzi.io/docs/0.7.0/

Topics are created via KafkaTopic resoruces in the associated OpenShift
Project, and the topics required for a baseline testing environment with the
Platform Upload and Engine services can be created by editing the `topics.json`
file in the topics directory to suit your environment and running the
accompanying python script.

From that point the OpenShift jobs in the tests directory can be altered for
your environment/project and run to ensure that messages are properly being
passed through the Kafka nodes to subscribed Consumers.

### Errors

Errors and fault tolerance are largely handled via OpenShift and Strimzi.

Containers determined to have failed (via the included health check endpoints)
will be scaled/restarted by OpenShift and the default three-node Kafka cluster
offers additional resiliance for failure/error scenarios.

## Getting Started

This Messaging Service, as primarily a deployment and configuration of an
existing product, development is something of a different concept than in other
Platform Services. The intent of this repository is to house the deployment,
setup, and simplification scripts needed for recreating and/or testing the
service as needed.

Propsed changes to the deployment scripts should be tested, where possible, in
an OpenShift environment comprable to OSD or OpenShift online, then submitted
as PRs.

### Deployment

Deployment of a test environment or redeployment is intended via the
`strimzi-cluster-operator.yaml` and `platform-mq-<env>.yaml` files. With
the `oc` command installed and working, the commands `oc apply -f
strimzi-cluster-operator.yaml -n <namespace>` will create an operator tasked
with watching for Strimzi `Kafka` resources. Following with `oc apply -f
platform-mq-<env>.yaml -n <namespace>` will stand up a replica environment.
Afterwards, running `create_topics.py -c <cluster_name> <namespace>` in the
`topics` directory will create the necessary testing topics in the new cluster
environment. Following this the test jobs in the `tests` directory can be run
to test message passing functionality.

## Additional Resources

### Kafka Conenct

    - **WIP**

### Avro Schema Registry

    - **WIP**

### Authentication and Authorization

    - **WIP**



## Authors

* **Chris Mitchell** - **Initial Work** - [wcmitchell](https://github.com/wcmitchell)
