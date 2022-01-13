FROM registry.redhat.io/amq7/amq-streams-kafka-28-rhel8:2.0.0-9
USER root:root
COPY ./connect-plugins/ /opt/kafka/plugins/
USER 1001
