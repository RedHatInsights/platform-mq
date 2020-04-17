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
Afterwards, running `create_topics.py -n <namespace>` in the
`topics` directory will create the necessary testing topics in the new cluster
environment. Following this the test jobs in the `tests` directory can be run
to test message passing functionality.

### Topics and Topic Creation

In our dev MQ instance, topics will be automatically created when produced to
or consumed from. Given the potential for chaos that this could create in
production, though, topic autocreation is locked down on non-dev MQ
environments. For those environments topic creation is still possible, but must
be done with intent via an administration interface. The simplest mechanism for
this will be to create a PR adding the new topic configuration to the
`topics.json` file. Once merged, a user with access to the OpenShift MQ projects
can use the `create_topics.py` script to sync the topic configs.

The following document contains the current and future plans for topics:

https://docs.google.com/spreadsheets/d/1xx_Zu7fnE8qEtd46vTohR5pyVibRD1-IRDWyj2tZnM0

**Note:** In addition to adding Kafka topics to the `topics.json` file, please follow instructions in [README](helm/README.md) to add topics to [vaules.yaml](helm/kafka-topics/values.yaml) and update the OpenShift [template](deploys/openshift/kafa-topics.yaml).

## Additional Resources

### Kafka Connect

    - **WIP**

### Avro Schema Registry

Alongside the Kafka deployment we have an Avro Schema Registry deployed. This
will allow us to have versioning and verifying of messages placed on the
associated topics. Some information on API calls for registering schemas
(written in JSON) to the registry is available at:

https://github.com/confluentinc/schema-registry

Generally, Avro/Schema Registry aware libraries must be used for
producing/consuming messages that adhere to a registered Avro schema. This may
require some additional code, but as we're using Confluent's Avro Schema
Registry image, their libraries should by and large be able to handle those
connections:

https://docs.confluent.io/current/clients/index.html

#### Avro Template/Schema Workflow

    1. Define topic schema (See sample in schemas subdir)
    2. Register schema with Avro Registry (see above docs or register_schema
       script in schemas subdir)
    3. Configure your producer to use an Avro serializer
        - **NB:** The schema is considered part and parcel to the message with
          Avro. This means you'll need the schema definition in your producer
          code somewhere.
    4. Move your consumers to Avro capable deserializers
    5. Messages to the registered topic using an Avro serializer will now be
       passed through the registry for verification before being delivered

### Authentication and Authorization

Strimzi's deploys provide us with a User Operator in addition to the Cluster
Operator tasked with keeping the Zookeeper ensemble and Kafka broker cluster
running and stable. With this operator, KafkaUser resources can be created to
generate appropriate certificates and ACLs for a given client application. With
the certs created, the client should then connect to the kafka-brokers service
at port 9093. As we work towards a production deployment, the expectations is
that non-authed access will be disabled in favor of only using the authed
service.



## Authors

* **Chris Mitchell** - **Initial Work** - [wcmitchell](https://github.com/wcmitchell)
