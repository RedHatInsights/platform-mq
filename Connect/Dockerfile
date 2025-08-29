FROM registry.redhat.io/amq-streams/kafka-38-rhel9:2.9.1-5

USER root:root

ENV KAFKA_CONNECT_PLUGINS_DIR=/opt/kafka/plugins \
    EXTERNAL_LIBS_DIR=/opt/kafka/libs \
    DEBEZIUM_VERSION=2.7.4.Final \
    GROOVY_VERSION=4.0.27 \
    RELATIONS_SINK_VERSION=0.5

RUN curl -sfSL --output-dir /usr/local/bin -o docker-maven-download.sh https://raw.githubusercontent.com/debezium/container-images/refs/heads/main/connect-base/3.0/docker-maven-download.sh && \
    chmod +x /usr/local/bin/docker-maven-download.sh

RUN mkdir -p $KAFKA_CONNECT_PLUGINS_DIR

# This one we can't easily pull from a maven repo
# COPY ./confluentinc-kafka-connect-s3-10.6.7 $KAFKA_CONNECT_PLUGINS_DIR

# Groovy plugins deps
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy "$GROOVY_VERSION" 5ed4a726792980fe8c6667e6824b0564
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy-jsr223 "$GROOVY_VERSION" c0fee136e61afee85920cee59ee1e36f
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/apache/groovy groovy-json "$GROOVY_VERSION" 2a1af97e9933da6186f596deec089ad7

# Kafka Relations Sink
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh central org/project-kessel kafka-relations-sink "$RELATIONS_SINK_VERSION" 9a9ceeaa6734969f54b049d02dfd1812

# Debezium Postgres Source
# io/debezium/debezium-connector-postgres/$DEBEZIUM_VERSION/debezium-connector-postgres-$DEBEZIUM_VERSION-plugin.tar.gz
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh debezium postgres "$DEBEZIUM_VERSION" 0dce7962ecae166afca16ec5fcd508f9
# io/debezium/debezium-scripting/$DEBEZIUM_VERSION/debezium-scripting-$DEBEZIUM_VERSION-plugin.tar.gz
RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh debezium-optional scripting "$DEBEZIUM_VERSION" 75fdd97f8c81636bc09948f306bc5882

RUN MAVEN_DEP_DESTINATION=$KAFKA_CONNECT_PLUGINS_DIR docker-maven-download.sh confluent kafka-connect-s3 "10.6.5" 948a8a86f4e8ff397dc9b72e1712d29e

USER 1001
