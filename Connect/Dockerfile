FROM registry.redhat.io/amq-streams/kafka-37-rhel9:2.7.0-19
USER root:root
RUN mkdir -p /opt/kafka/plugins/
WORKDIR /opt/kafka/plugins/
RUN curl https://maven.repository.redhat.com/ga/io/debezium/debezium-connector-postgres/2.5.4.Final-redhat-00001/debezium-connector-postgres-2.5.4.Final-redhat-00001-plugin.zip -o debezium-connector-postgres-2.5.4.Final-redhat-00001-plugin.zip && unzip debezium-connector-postgres-2.5.4.Final-redhat-00001-plugin.zip && rm debezium-connector-postgres-2.5.4.Final-redhat-00001-plugin.zip
RUN curl https://maven.repository.redhat.com/ga/io/debezium/debezium-scripting/2.5.4.Final-redhat-00001/debezium-scripting-2.5.4.Final-redhat-00001.zip -o debezium-scripting-2.5.4.Final-redhat-00001.zip && unzip debezium-scripting-2.5.4.Final-redhat-00001.zip && rm debezium-scripting-2.5.4.Final-redhat-00001.zip
RUN curl https://repo1.maven.org/maven2/org/apache/groovy/groovy/4.0.22/groovy-4.0.22.jar -o groovy-4.0.22.jar
RUN curl https://repo1.maven.org/maven2/org/apache/groovy/groovy-jsr223/4.0.22/groovy-jsr223-4.0.22.jar -o groovy-jsr223-4.0.22.jar
RUN curl https://repo1.maven.org/maven2/org/apache/groovy/groovy-json/4.0.22/groovy-json-4.0.22.jar -o groovy-json-4.0.22.jar
RUN curl https://maven.repository.redhat.com/ga/org/apache/camel/kafkaconnector/camel-aws-s3-kafka-connector/0.7.1.fuse-800004-redhat-00001/camel-aws-s3-kafka-connector-0.7.1.fuse-800004-redhat-00001-package.zip -o camel-aws-s3-kafka-connector-0.7.1.fuse-800004-redhat-00001-package.zip && unzip camel-aws-s3-kafka-connector-0.7.1.fuse-800004-redhat-00001-package.zip && rm camel-aws-s3-kafka-connector-0.7.1.fuse-800004-redhat-00001-package.zip 
RUN curl https://repo1.maven.org/maven2/org/project-kessel/kafka-relations-sink/0.3/kafka-relations-sink-0.3.jar -o kafka-relations-sink-0.3.jar
WORKDIR /opt/kafka/
USER 1001
