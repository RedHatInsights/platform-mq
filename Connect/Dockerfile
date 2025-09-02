FROM registry.redhat.io/amq-streams/kafka-38-rhel9:2.9.1-5

USER root:root

ENV KAFKA_CONNECT_PLUGINS_DIR=/opt/kafka/plugins \
    EXTERNAL_LIBS_DIR=/opt/kafka/libs \
    DEBEZIUM_VERSION=3.2.1.Final \
    GROOVY_VERSION=5.0.0 \
    RELATIONS_SINK_VERSION=0.5

RUN curl -sfSL --output-dir /usr/local/bin -o docker-maven-download.sh https://raw.githubusercontent.com/debezium/container-images/refs/heads/main/connect-base/3.0/docker-maven-download.sh && \
    chmod +x /usr/local/bin/docker-maven-download.sh

RUN mkdir -p $KAFKA_CONNECT_PLUGINS_DIR

# Groovy plugins deps
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy "$GROOVY_VERSION" 1e636c3520585172571980d545e84845
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy-json "$GROOVY_VERSION" 1c6f480c73719be5f81d1782eb0f25eb
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy-jsr223 "$GROOVY_VERSION" 0b9620ad36e6176672ca3b6dc1a7d244

# Kafka Relations Sink
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/project-kessel kafka-relations-sink "$RELATIONS_SINK_VERSION" 9a9ceeaa6734969f54b049d02dfd1812

# Debezium Postgres Source
# io/debezium/debezium-connector-postgres/$DEBEZIUM_VERSION/debezium-connector-postgres-$DEBEZIUM_VERSION-plugin.tar.gz
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh debezium postgres "$DEBEZIUM_VERSION" 9ab417e37bee225e8440862749c755dd
# io/debezium/debezium-scripting/$DEBEZIUM_VERSION/debezium-scripting-$DEBEZIUM_VERSION.tar.gz
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh debezium-optional scripting "$DEBEZIUM_VERSION" 6afda020b3432fcb7f17e3ed814dbf13

RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh confluent kafka-connect-s3 "10.6.5" 948a8a86f4e8ff397dc9b72e1712d29e

USER 1001
