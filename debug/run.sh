#! /bin/bash

echo "---"
id
echo "---"

envsubst < /opt/kafka/config/authed-kafka.properties.template > /opt/kafka/config/authed-kafka.properties

sleep infinity
