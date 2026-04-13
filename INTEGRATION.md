# Platform-MQ Integration with App-Interface

This document describes how Platform-MQ integrates with app-interface for deployment and configuration.

## Overview

Platform-MQ provides OpenShift templates and configuration for managing Kafka resources (topics, connectors, operators) that run in OpenShift and interact with AWS MSK clusters. The actual deployment of these resources is managed through app-interface.

## Architecture

### Three-Repository Model

The Kafka platform uses a hybrid architecture spanning three repositories:

```
┌─────────────────────┐
│  third-party-       │  Provides: AMQ Streams Operator (OLM subscription)
│  operators          │  Deploys: Operator to OpenShift clusters
│  (GitLab)           │  Owner: AppSRE shared infrastructure
│                     │  URL: gitlab.cee.redhat.com/insights-platform/third-party-operators
└──────────┬──────────┘
           │
           │ Operator installed
           ▼
┌─────────────────────┐
│  platform-mq        │  Provides: OpenShift templates, topic definitions
│  (THIS REPO)        │  Deploys: Via app-interface references
│  (GitHub)           │  Owner: Kafka platform team
│                     │  URL: github.com/RedHatInsights/platform-mq
└──────────┬──────────┘
           │
           │ Templates referenced
           ▼
┌─────────────────────┐
│  app-interface      │  Provides: Configuration, external resources, targets
│  (GitLab)           │  Deploys: Everything via OpenShift-SaaS-Deploy
│                     │  Owner: AppSRE
│                     │  URL: gitlab.cee.redhat.com/service/app-interface
└─────────────────────┘
```

### Deployment Flow

1. **AMQ Streams Operator Installation**:
   - `third-party-operators/amq-streams.yml` defines OLM subscription
   - `app-interface/data/services/insights/third-party-operators/deploy.yml` deploys subscription to clusters
   - OLM installs operator and CRDs (KafkaTopic, KafkaConnect, etc.)

2. **MSK Cluster Provisioning**:
   - `app-interface/data/services/insights/strimzi/namespaces/*.yml` define MSK external resources
   - External Resources v2 integration provisions MSK clusters via Terraform
   - SASL/SCRAM users created and credentials stored in Vault

3. **Strimzi Component Deployment**:
   - `platform-mq/deploys/openshift/*.yaml` templates define Strimzi resources
   - `app-interface/data/services/insights/strimzi/saas.yml` references these templates
   - OpenShift-SaaS-Deploy deploys to target namespaces
   - AMQ Streams operator reconciles CRs and creates OpenShift resources

## App-Interface Integration Points

### SaaS File Configuration

**Location**: `app-interface/data/services/insights/strimzi/saas.yml`

This file defines all resource templates and deployment targets:

```yaml
resourceTemplates:
- name: platform-kafka-connect
  path: /deploys/openshift/aio_connect_auth.yaml    # Path in THIS repo
  url: https://github.com/RedHatInsights/platform-mq # THIS repo
  targets:
  - namespace:
      $ref: /services/insights/strimzi/namespaces/platform-mq-prod.yml
    ref: 8bb5731                                     # Git commit SHA
    parameters:
      IMAGE_TAG: 8bb5731                             # Parameter overrides
```

**Key Fields**:
- **path**: Relative path to template in this repository
- **url**: This repository URL
- **ref**: Git commit SHA (production) or branch (stage/dev)
- **parameters**: Template parameter overrides
- **secretParameters**: Vault secrets injected as parameters

### Deployment Targets

Each template deployment targets one or more namespaces:

**Namespace Definition** (in app-interface):
```yaml
# data/services/insights/strimzi/namespaces/platform-mq-prod.yml
name: platform-mq-prod
cluster:
  $ref: /openshift/crcp01ue1/cluster.yml

externalResources:
  - provider: msk
    identifier: consoledot-prod
    output_resource_name: consoledot-prod-msk
    users:
      - name: scram-admin-prod
        secret:
          path: insights/secrets/insights-prod/msk-credentials/admin
```

This defines:
- Which OpenShift cluster hosts the namespace
- MSK cluster connection details
- SASL/SCRAM credentials for authentication

### Templates in This Repository

| Template | Purpose | Deployed To | App-Interface Reference |
|----------|---------|-------------|------------------------|
| `aio_connect_auth.yaml` | Kafka Connect with auth | platform-mq-{stage\|prod} | saas.yml (platform-kafka-connect) |
| `kafka-topic-operator.yaml` | Standalone topic operator | kafka-topics-{stage\|prod} | saas.yml (standalone-topic-operator) |
| `kafka-topics.yaml` | All KafkaTopic definitions | kafka-topics-{stage\|prod} | saas.yml (kafka-topics) |
| `kafka-connectors.yaml` | KafkaConnector resources | platform-mq-{stage\|prod} | saas.yml (kafka-connector-*) |
| `kafka-bridge.yml` | HTTP bridge to Kafka | stage-platform-mq-stage | saas.yml (kafka-bridge) |
| `msk-to-msk-mm2.yaml` | MirrorMaker2 replication | platform-mq-{stage\|prod} | saas.yml (assisted-installer-mirrormaker) |

## Development Workflow

### Making Changes to Templates

#### Stage/Development Changes (Auto-Deploy)

1. **Update template** in this repository:
   ```bash
   git checkout -b feature/my-change
   # Edit deploys/openshift/aio_connect_auth.yaml
   git commit -m "Update Kafka Connect memory limits"
   git push origin feature/my-change
   ```

2. **Create PR and merge** to `main` branch

3. **Auto-deployment to stage**:
   - App-interface saas.yml references `ref: main` for stage targets
   - OpenShift-SaaS-Deploy detects change and deploys automatically
   - Changes appear in stage within minutes

#### Production Changes (Controlled Promotion)

1. **Verify in stage** that changes work correctly

2. **Create app-interface PR** to update production reference:
   ```yaml
   # app-interface/data/services/insights/strimzi/saas.yml
   - namespace:
       $ref: /services/insights/strimzi/namespaces/platform-mq-prod.yml
     ref: abc123def456  # Update to commit SHA from step 1
   ```

3. **App-interface PR review and merge**

4. **Production deployment**:
   - OpenShift-SaaS-Deploy deploys the pinned commit to production
   - Production remains stable on specific commits

**Why This Flow?**
- Stage gets continuous deployment for rapid iteration
- Production gets controlled deployments with explicit approvals
- Rollbacks are easy: revert app-interface PR to previous commit SHA

### Adding New Resources

#### Example: Add a New Kafka Connector

1. **Create connector template** in this repo:
   ```yaml
   # deploys/openshift/my-new-connector.yaml
   apiVersion: v1
   kind: Template
   parameters:
   - name: CONNECTOR_NAME
     required: true
   - name: TOPICS
     required: true
   objects:
   - apiVersion: kafka.strimzi.io/v1beta2
     kind: KafkaConnector
     metadata:
       name: ${CONNECTOR_NAME}
       labels:
         strimzi.io/cluster: platform-kafka-connect
     spec:
       class: io.confluent.connect.s3.S3SinkConnector
       config:
         topics: ${TOPICS}
   ```

2. **Commit and push** to this repo

3. **Add resource template to app-interface**:
   ```yaml
   # app-interface/data/services/insights/strimzi/saas.yml
   resourceTemplates:
   - name: my-new-connector-stage
     path: /deploys/openshift/my-new-connector.yaml
     url: https://github.com/RedHatInsights/platform-mq
     parameters:
       CONNECTOR_NAME: my-new-connector
       TOPICS: my.topic.name
     targets:
     - namespace:
         $ref: /services/insights/strimzi/namespaces/stage-platform-mq-stage.yml
       ref: main
   ```

4. **Deploy to stage** (via app-interface PR)

5. **Promote to production** (add production target with pinned ref)

## Topic Management

### Topic Definition Process

Topics are NOT defined directly in OpenShift templates. Instead:

1. **Define in Helm values**:
   ```yaml
   # helm/kafka-topics/values.yaml
   topics:
     - name: my.new.topic
       cluster: msk_prod
       partitions: 3
       replicationFactor: 3
       config:
         retention.ms: "604800000"
   ```

2. **GitHub Actions generates template**:
   - `.github/workflows/` runs Helm template on PR merge
   - Outputs to `deploys/openshift/kafka-topics.yaml`
   - Commits generated file back to repo

3. **App-interface deploys**:
   - References `kafka-topics.yaml` in saas.yml
   - Deploys KafkaTopic CRs to `kafka-topics-{stage|prod}` namespaces
   - Topic operator creates actual topics on MSK

**See**: `helm/README.md` for detailed topic management workflow

## Secret Management

### Vault Secrets

MSK credentials and other secrets are stored in Vault and referenced in app-interface:

**Secret Definition** (in app-interface namespace):
```yaml
# data/services/insights/strimzi/namespaces/platform-mq-prod.yml
openshiftResources:
- provider: vault-secret
  path: insights/secrets/insights-prod/msk-credentials/admin
  version: 1
```

**Secret Usage** (in app-interface saas.yml):
```yaml
secretParameters:
- name: BOOTSTRAP_SERVERS
  secret:
    path: insights/secrets/insights-prod/msk-credentials/consoledot-prod-msk
    field: bootstrap_brokers_sasl_scram
    version: 1
```

**In Template** (in this repo):
```yaml
# deploys/openshift/aio_connect_auth.yaml
parameters:
- name: BOOTSTRAP_SERVERS
  required: true

objects:
- spec:
    bootstrapServers: ${BOOTSTRAP_SERVERS}
```

**Flow**:
1. Vault secret contains `bootstrap_brokers_sasl_scram` field
2. App-interface injects secret field value as `BOOTSTRAP_SERVERS` parameter
3. Template uses parameter to configure resource
4. No secrets stored in this repository or app-interface YAML

### Credentials Available

**MSK Credentials** (per environment):
- **admin**: Full cluster admin (topic CRUD, ACLs, configs)
- **client**: Application read/write access
- **mirrormaker**: Cross-cluster replication

**Secret Paths**:
- Stage: `insights/secrets/insights-stage/msk-credentials/{admin|client|mirrormaker}`
- Prod: `insights/secrets/insights-prod/msk-credentials/{admin|client|mirrormaker}`

## Custom Images

### Kafka Connect Image

**Build Location**: `Connect/Dockerfile`

**Includes**:
- Base: Red Hat AMQ Streams Kafka Connect image
- Plugins: Confluent S3 Sink (10.6.7), custom transforms

**Build Process**:
1. Update `Connect/Dockerfile` or plugins
2. CI/CD pipeline builds and pushes to `quay.io/cloudservices/kafka-connect`
3. Update app-interface saas.yml with new image tag
4. Deploy via app-interface

**Image Tag Strategy**:
- Stage: `latest` (auto-updates)
- Production: Pinned tag (e.g., `8bb5731`)

## Monitoring Integration

### Metrics

**Kafka Connect Metrics**:
- Template: `deploys/openshift/kafka-connect-metrics-configmap.yaml`
- Deployed to: platform-mq-{stage|prod} namespaces
- Configures JMX exporter in Connect pods

**Consumer Lag Monitoring**:
- Template: `deploys/openshift/lightbend-lag-exporter.yaml`
- Monitors consumer group lag across all topics
- Exports Prometheus metrics

### Dashboards

**MSK Dashboards**:
- Defined in: `app-interface/data/services/insights/strimzi/saas-consoledot-msk-dashboards.yml`
- Deployed to: Grafana instances
- Metrics from: CloudWatch (MSK), Prometheus (exporters)

## Namespace Organization

### App-Interface Namespaces

| Namespace | Cluster | Purpose | Templates Deployed |
|-----------|---------|---------|-------------------|
| platform-mq-prod | crcp01ue1 | Production Kafka Connect | aio_connect_auth, kafka-connectors, msk-to-msk-mm2 |
| stage-platform-mq-stage | stage cluster | Stage Kafka Connect | aio_connect_auth, kafka-connectors, kafka-bridge |
| kafka-topics-prod | crcp01ue1 | Production topic management | kafka-topic-operator, kafka-topics |
| kafka-topics-stage | stage cluster | Stage topic management | kafka-topic-operator, kafka-topics |

### Template-to-Namespace Mapping

Each template can target multiple namespaces with different parameters:

```yaml
# Same template, different configs per environment
- name: kafka-connector-warehouse-sink
  path: /deploys/openshift/kafka-connectors.yaml
  targets:
  - namespace:
      $ref: .../stage-platform-mq-stage.yml
    parameters:
      S3_SINK_BUCKET_NAME: insights-warehouse-stage
  - namespace:
      $ref: .../platform-mq-prod.yml
    parameters:
      S3_SINK_BUCKET_NAME: insights-warehouse-prod
```

## Testing Changes

### Local Development

1. **Render template locally**:
   ```bash
   oc process -f deploys/openshift/aio_connect_auth.yaml \
     -p KAFKA_CONNECT_VERSION=3.8.0 \
     -p AUTH_CLIENT_SECRET_NAME=admin \
     -o yaml
   ```

2. **Validate with oc**:
   ```bash
   oc process -f deploys/openshift/aio_connect_auth.yaml \
     -p KAFKA_CONNECT_VERSION=3.8.0 \
     --dry-run=client -o yaml | oc apply --dry-run=client -f -
   ```

### CRCD (Development Cluster)

Some resources have CRCD deployments for testing:

- AMQ Streams operator deployed to CRCD cluster
- Standalone topic operator: `data/services/insights/third-party-operators/kafka-topic-operator/crcd.yml`
- Connected to CRCD-specific MSK cluster

**To test in CRCD**:
1. Update template in this repo
2. Update app-interface CRCD namespace reference to new commit
3. Verify in CRCD cluster

## Troubleshooting

### Template Not Deploying

**Check OpenShift-SaaS-Deploy logs**:
- Pipeline runs in `strimzi-pipelines` namespace
- Look for template processing errors
- Verify all required parameters are provided

**Common Issues**:
- Missing parameter in app-interface saas.yml
- Invalid template syntax (check with `oc process`)
- Namespace doesn't exist or isn't accessible

### Parameters Not Applied

**Verify parameter flow**:

1. **Check template defines parameter**:
   ```yaml
   parameters:
   - name: MY_PARAM
     required: true
   ```

2. **Check app-interface provides parameter**:
   ```yaml
   parameters:
     MY_PARAM: my-value
   ```

3. **Check template uses parameter**:
   ```yaml
   spec:
     config: ${MY_PARAM}
   ```

### Secrets Not Available

**Verify secret path**:
1. Check Vault path exists: `vault kv get <path>`
2. Check namespace has vault-secret resource
3. Check secretParameters in app-interface references correct path
4. Verify secret version matches

## References

- **App-Interface Repository**: https://gitlab.cee.redhat.com/service/app-interface
  - Architecture overview: `docs/tenant-services/strimzi/architecture.md`
  - Operations guide: `docs/tenant-services/strimzi/operations.md`
  - SaaS File: `data/services/insights/strimzi/saas.yml`
  - Namespaces: `data/services/insights/strimzi/namespaces/`
- **Third-Party Operators Repository**: https://gitlab.cee.redhat.com/insights-platform/third-party-operators
  - AMQ Streams Operator: `amq-streams.yml`
  - Deployment config: `kafka-topic-operator.yaml`
