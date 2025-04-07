FROM registry.redhat.io/amq-streams/kafka-38-rhel9:2.9.0-3 AS build-image

USER root:root

ENV KAFKA_CONNECT_PLUGINS_DIR=/opt/kafka/plugins \
    EXTERNAL_LIBS_DIR=/opt/kafka/libs \
    DEBEZIUM_VERSION=2.7.3.Final \
    GROOVY_VERSION=4.0.22 \
    RELATIONS_SINK_VERSION=0.4

# commonly used for getting maven connect plugins
RUN curl -sfSL --output-dir /usr/local/bin -o docker-maven-download.sh https://raw.githubusercontent.com/debezium/container-images/refs/heads/main/connect-base/3.0/docker-maven-download.sh && \
    chmod +x /usr/local/bin/docker-maven-download.sh

RUN mkdir -p $KAFKA_CONNECT_PLUGINS_DIR

# Can't pull this one easily from a repo
COPY ./Connect/confluentinc-kafka-connect-s3-10.5.17 $KAFKA_CONNECT_PLUGINS_DIR

# Groovy plugins deps
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy "$GROOVY_VERSION" b527c6bfa1af469f1a4374e9fc6de4bf
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy-jsr223 "$GROOVY_VERSION" c2dbd84cfeb6bb93ea8253af3af2adca
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy-json "$GROOVY_VERSION" 86f2d4325465f5b747d6c2cd159b36c0

# Kafka Relations Sink
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/project-kessel kafka-relations-sink "$RELATIONS_SINK_VERSION" a4088bb1c7298ac0144056c14fd522ce

# Debezium Postgres Source
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh debezium postgres "$DEBEZIUM_VERSION" 9bb46566fa18541be206f0bd0f77c4de
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh debezium-optional scripting "$DEBEZIUM_VERSION" e8c6825ada56c4f028b67fe634f7d4d6

USER 1001
