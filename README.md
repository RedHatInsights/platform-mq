# Insights Platform Messaging Service

This Messaging Service is designed to work as the piping between various
Platform client services.

## Details

The Messaging Service backs the different components of Insights Platform to
allow for cross-application and intra-application communication. This is
achieved with an OpenShift based deployment of Apache's Kafka message queue as
deployed and orchestrated by the forthcoming AMQ Streams Red Hat project.

Currently we're running the upstream product for AMQ Streams, Strimzi, at
version 0.4.0.

The service runs entirely in Openshift Dedicated.

## How it Works

The Messaging Service is a standard deployment of Apache Kafka orchestrated by
Strimzi. Product documentation is available at:

http://strimzi.io/docs/0.4.0/

Topics are created via ConfigMaps in the associated OpenShift Project, and the
topics required for a baseline testing environment with the Platform Upload and
Engine services can be created by editing the `generate.py` script in the
topics directory to suit your environment.

From that point the OpenShift jobs in the tests directory can be altered for
your environment/project and run to ensure that messages are properly being
passed through the Kafka nodes to subscribed Consumers.

### Errors

Errors and fault tolerance are largely handled via OpenShift and Strimzi.

Failing pods will be restarted and the default three-node Kafka cluster offers
additional resiliance for failure/error scenarios. 

## Getting Started

**WIP** Local development and testing documentation in progress.

## Running with Tests

Any new features added to the application should be accompanied by a Unittest in `./tests`

## Deployment

**WIP** - the QA and Production projects are not in place yet. The project is deployed on
`Platform-MQ` only

## Contributing

All outstanding issues or feature requests should be filed as Issues on this Github
page. PRs should be submitted against the master branch for any new features or changes.

## Authors

* **Chris Mitchell** - **Initial Work** - [wcmitchell](https://github.com/wcmitchell)
