# Migration to msk-debug-container

## Summary

Migrated from custom-built `quay.io/cloudservices/kafka-debug` to the App-SRE maintained `msk-debug-container`.

## Changes Made

### Updated Files
- **kafka-debug-pod.yml**: 
  - Image changed to `quay.io/redhat-user-workloads/app-sre-tenant/container-images-master/msk-debug-container-master:3.8`
  - Env vars renamed: `BOOTSTRAP_SERVERS` → `MSK_BOOTSTRAP_SERVERS`, `KAFKA_USERNAME` → `MSK_USER`, `KAFKA_PASSWORD` → `MSK_PASSWORD`

### Files That Can Be Removed

These files are no longer needed as msk-debug-container provides the same functionality:

- ❌ `Dockerfile` - Previously built custom image
- ❌ `authed-kafka.properties.template` - Replaced by msk-debug-container's `/client.properties.template`
- ❌ `run.sh` - Replaced by msk-debug-container's `/start.sh`

**Before removing**, verify that:
1. No CI/CD pipelines reference these files
2. `quay.io/cloudservices/kafka-debug` image builds are no longer needed
3. All existing deployments have been updated to use the new image

## Verification Steps

1. Deploy the updated template to a test namespace:
   ```bash
   oc process --local \
     -p KAFKA_ACCESS_SECRET_NAME=your-access-secret \
     -p KAFKA_AUTH_SECRET_NAME=your-auth-secret \
     -f kafka-debug-pod.yml | oc apply -f -
   ```

2. Verify the pod starts successfully:
   ```bash
   oc get pods -l app=kafka-debug
   oc logs deployment/kafka-debug
   ```

3. Test Kafka connectivity:
   ```bash
   oc rsh deployment/kafka-debug
   # Inside the pod:
   kafka-topics.sh --bootstrap-server $MSK_BOOTSTRAP_SERVERS --command-config $MSK_CONFIG --list
   ```

## Rollback Plan

If issues arise, the old image is still available:
- Image: `quay.io/cloudservices/kafka-debug:latest`
- Revert env var names back to: `BOOTSTRAP_SERVERS`, `KAFKA_USERNAME`, `KAFKA_PASSWORD`
