# Kafka Debug Container

This deployment uses the **msk-debug-container** from the app-sre/container-images repository instead of maintaining a separate kafka-debug image.

## Image

- **Image**: `quay.io/redhat-user-workloads/app-sre-tenant/container-images-master/msk-debug-container-master`
- **Source**: https://github.com/app-sre/container-images/tree/master/msk-debug-container
- **Quay Repository**: https://quay.io/repository/redhat-user-workloads/app-sre-tenant/container-images-master/msk-debug-container-master?tab=tags

## Deprecated Files

The following files are no longer used and can be removed:
- `Dockerfile` - Previously built custom kafka-debug image
- `authed-kafka.properties.template` - Replaced by msk-debug-container's client.properties.template
- `run.sh` - Replaced by msk-debug-container's start.sh

The msk-debug-container handles authentication setup automatically using the same secret structure.

## Usage

Deploy the debug container:

```bash
oc login ...
oc project <namespace>

# Deploy with your secrets
oc process --local \
  -p KAFKA_ACCESS_SECRET_NAME=<your-kafka-access-secret> \
  -p KAFKA_AUTH_SECRET_NAME=<your-kafka-auth-secret> \
  -f kafka-debug-pod.yml | oc apply -f -

# Connect to the pod
oc rsh deployment/kafka-debug
```

Inside the container, Kafka tools are available:

```bash
# The MSK_CONFIG env var points to the auto-generated client.properties
kafka-topics.sh --bootstrap-server $MSK_BOOTSTRAP_SERVERS --command-config $MSK_CONFIG --list

# Consume from a topic
kafka-console-consumer.sh --bootstrap-server $MSK_BOOTSTRAP_SERVERS \
  --consumer.config $MSK_CONFIG \
  --topic my-topic --from-beginning

# Produce to a topic
kafka-console-producer.sh --bootstrap-server $MSK_BOOTSTRAP_SERVERS \
  --producer.config $MSK_CONFIG \
  --topic my-topic
```

## Environment Variables

The msk-debug-container expects:
- `MSK_BOOTSTRAP_SERVERS` - Kafka bootstrap servers
- `MSK_USER` - SASL username
- `MSK_PASSWORD` - SASL password
- `MSK_CONFIG` - Path to client config (default: `/client.properties`)

These are populated from the secrets specified in the template parameters.
