# Platform-MQ Operations Runbook

Operational procedures for managing the ConsoleDot Kafka/MSK infrastructure.

## Topic PR Reviews

Topic changes follow a self-service PR model. A GitHub Action automatically runs Helm generation, so reviewers don't need to worry about that step.

**Review checklist:**

- Topic name is unique (not duplicating an existing topic)
- Partition count is specified and reasonable (upper bound ~64; monitor total partition count across the cluster to stay within MSK limits)
- Replication factor is 3
- If `retention.bytes` is set: generally should be under 1 GB
- If `retention.ms` is set: generally should be 7 days or less

High retention values aren't an automatic rejection but should prompt a conversation with the requesting team about their use case.

### Production Promotion

Topic changes auto-deploy to stage (saas.yml `ref: main`), but production requires updating the kafka-topics SHA in `data/services/insights/strimzi/saas.yml` in app-interface — the same promotion workflow as Connect image updates.

## Connector / Connect Image Updates

The Kafka Connect image bundles the Connect runtime and connector plugins (e.g., Confluent S3 Sink) into a single image built from `Connect/Dockerfile`.

### CVE Response Workflow

1. **Try a UBI base image bump first.** Update the base image in `Connect/Dockerfile` — this resolves most CVE alerts.
2. **If the CVE is in a connector dependency**, find the latest version on Maven Central, update the version string in the `ENV` stanza of the Dockerfile, and update the corresponding md5sum in the `docker-maven-download.sh` invocation (the checksum is typically available alongside the artifact in Maven).
3. **Create a PR.** Konflux runs two pre-merge checks:
   - Image build validation
   - Enterprise contract verification (ensures Konflux task bundles are current)
4. **Merge to main.** Triggers the Konflux build-and-release pipeline, which auto-deploys the new image to **stage**.
5. **Promote to prod.** Update the image SHA in `data/services/insights/strimzi/saas.yml` in app-interface to deploy to production.

## Troubleshooting

Most reported issues trace back to client-side configuration or behavior rather than the Kafka brokers themselves. However, thorough diagnosis is important — start from the brokers and work outward to confirm.

### Diagnostic Flow

**1. Check operator pods**

| Component | Namespace | Cluster |
|-----------|-----------|---------|
| AMQ Streams Operator | `amq-streams` | crcs (stage) / crcp (prod) |
| Strimzi Topic Operator | `kafka-topics-stage` / `kafka-topics-prod` | crcs / crcp |
| Kafka Connect | `platform-mq-stage` / `platform-mq-prod` | crcs / crcp |

For each: check for pod restarts, review events, read pod logs.

**2. Check broker logs**

MSK broker logs are in AWS CloudWatch:

| Environment | AWS Account | Log Stream |
|-------------|-------------|------------|
| Stage | crc-stage | `consoledot-stage-msk-broker-logs` |
| Production | insights-prod-rh | `consoledot-prod-msk-broker-logs` |

### Consumer Lag

Consumer lag reports are almost always a client-side issue. Diagnostic steps:

1. Get the consumer group ID from the reporting team
2. Check broker logs for rebalance messages for that consumer group
3. Review CloudWatch metrics dashboards (Grafana: `grafana.app-sre.devshift.net` > AWS Apache Kafka MSK) to determine if the lag is transient or persistent
4. Resolution is typically client-side fixes (pod stability, consumer configuration, rebalance tuning)

## Incident Response

### Current State

There is no formal severity classification, on-call rotation, or dedicated issue-reporting mechanism for platform-mq. Historically, issues have been surfaced reactively via chat pings and alerts.

**Recommendation for the new owning team:** Establish a lightweight incident process — even a simple Slack channel + severity tagging would be an improvement over the current ad-hoc model.

### Existing Alerts

PrometheusRule alerts are defined in app-interface (`resources/insights-{stage,prod}/strimzi/msk.prometheusrules.yml`):

| Alert | Condition | Severity |
|-------|-----------|----------|
| MSKBrokerCount | Fewer than 3 brokers for 10 min | high |
| MSKStorageUsageHigh | Broker disk usage > 70% for 10 min | high |
| MSKStorageUsageCritical | Broker disk usage > 90% for 10 min | critical (prod) / high (stage) |

All alerts link to the [Grafana MSK dashboard](https://grafana.stage.devshift.net/d/adqkf8ktn86wwa/consoledot-msk) and the AWS MSK console.

**Gaps to consider filling:**
- Consumer lag alerts
- Connector failure/restart alerts
- Topic operator health alerts

## Access Management

### Credential Model

Each MSK environment has two credential tiers:

| Credential | Purpose | Used By |
|------------|---------|---------|
| **admin** | Full cluster access | Operators, MirrorMaker, topic operator |
| **client** | ACL-restricted access | Application microservices |

All credentials are stored in Vault and injected via app-interface secret mounts.

### Onboarding a New Service

**Clowderized apps (standard path):** Declare Kafka access in the app's ClowdApp CR. Clowder automatically injects the client credentials — no manual steps required.

**Non-Clowderized apps:** Mount the appropriate Vault secret via `secretParameters` in the app's app-interface namespace file.

There is no manual credential provisioning workflow. Per-service credentials and fine-grained ACLs were considered but not implemented due to operational overhead; the two-tier model has been sufficient at current scale.
