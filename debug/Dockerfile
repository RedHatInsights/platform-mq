FROM registry.redhat.io/amq-streams/kafka-36-rhel8:2.6.0-4
USER root:root
COPY ./authed-kafka.properties /opt/kafka/bin
RUN sh -c 'touch /opt/kafka/kafka.client.truststore.jks'
USER 1001
