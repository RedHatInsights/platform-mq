FROM registry.redhat.io/amq-streams/kafka-37-rhel9:2.7.0-5
USER root:root
COPY ./connect-plugins/ /opt/kafka/plugins/
USER 1001
