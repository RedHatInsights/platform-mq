FROM registry.redhat.io/amq-streams/kafka-38-rhel9:2.9.3-7

USER root:root

ENV KAFKA_CONNECT_PLUGINS_DIR=/opt/kafka/plugins \
    EXTERNAL_LIBS_DIR=/opt/kafka/libs \
    DEBEZIUM_VERSION=3.2.2.Final \
    GROOVY_VERSION=5.0.0 \
    RELATIONS_SINK_VERSION=0.6

RUN curl -sfSL --output-dir /usr/local/bin -o docker-maven-download.sh https://raw.githubusercontent.com/debezium/container-images/refs/heads/main/connect-base/3.0/docker-maven-download.sh && \
    chmod +x /usr/local/bin/docker-maven-download.sh

RUN mkdir -p $KAFKA_CONNECT_PLUGINS_DIR

# This one we can't easily pull from a maven repo
COPY confluentinc-kafka-connect-s3-10.6.7 $KAFKA_CONNECT_PLUGINS_DIR

# Groovy plugins deps
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy "$GROOVY_VERSION" 1e636c3520585172571980d545e84845
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy-json "$GROOVY_VERSION" 1c6f480c73719be5f81d1782eb0f25eb
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy-jsr223 "$GROOVY_VERSION" 0b9620ad36e6176672ca3b6dc1a7d244

# Kafka Relations Sink
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/project-kessel kafka-relations-sink "$RELATIONS_SINK_VERSION" 8a21ffe702ae2d06112a5595a9d8b843

# Debezium Postgres Source
# io/debezium/debezium-connector-postgres/$DEBEZIUM_VERSION/debezium-connector-postgres-$DEBEZIUM_VERSION-plugin.tar.gz
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh debezium postgres "$DEBEZIUM_VERSION" 7aab67711a68e69e27265aa36ec82f89
# io/debezium/debezium-scripting/$DEBEZIUM_VERSION/debezium-scripting-$DEBEZIUM_VERSION.tar.gz
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh debezium-optional scripting "$DEBEZIUM_VERSION" 06a42901cdc7fce560407b356b608697

USER 1001
