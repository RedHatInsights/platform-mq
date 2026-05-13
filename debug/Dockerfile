FROM registry.redhat.io/amq-streams/kafka-38-rhel9:2.9.3-28
USER root:root
COPY ./authed-kafka.properties.template /opt/kafka/config/
RUN touch /opt/kafka/config/authed-kafka.properties
RUN chmod 777 /opt/kafka/config/authed-kafka.properties
COPY ./run.sh /bin/
RUN chmod 755 /bin/run.sh
USER 1001
ENTRYPOINT ["/bin/run.sh"]
