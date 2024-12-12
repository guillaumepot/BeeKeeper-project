# Monitoring Documentation


# Monitoring Services Documentation

The following document describes the monitoring services used in the system.

## Information
- **Current Version:** v1
- **Stage:** In Development
- **Last doc update:** 2024-11-12

## Table of Contents
1. [Introduction](#introduction)
2. [Monitoring Services](#monitoring-services)
    - [Loki](#loki)
    - [Prometheus](#prometheus)
    - [Alertmanager](#alertmanager)
    - [Tempo](#tempo)
    - [Grafana](#grafana)
    - [MongoDB Exporter](#mongodb-exporter)
    - [Postgres Exporter](#postgres-exporter)
    - [Redis Exporter](#redis-exporter)
    - [StatsD Exporter](#statsd-exporter)
    - [Node Exporter](#node-exporter)
    - [cAdvisor](#cadvisor)

## Introduction

This section describes the various monitoring microservices used in the system, their roles, and their configurations. These services help monitor the performance, logs, and metrics of other microservices.

## Monitoring Services

### Loki

**Description:** Loki is used for log management. It collects and indexes logs from various services.

- **Image:** `grafana/loki:3.0.0`
- **Command:** `-config.file=/etc/loki/local-config.yaml`
- **Ports:** `3100`
- **Networks:** `beegis_monitoring_network`, `beegis_public_network`
- **Profiles:** `monitoring`, `loki`
- **Labels:**
  - `com.example.description`: "Container using Loki engine"
  - `com.example.department`: "BeeGis"

### Prometheus

**Description:** Prometheus is used for collecting and storing metrics from various services.

- **Image:** `prom/prometheus:v2.51.2`
- **Ports:** `9090`
- **Volumes:** `${PROMETHEUS_SOURCE_DIRECTORY}:/workspace`
- **Command:**
  - `--config.file=/workspace/prometheus.yml`
  - `--enable-feature=exemplar-storage`
- **Depends_on:** `loki`
- **Networks:** `beegis_airflow_network`, `beegis_monitoring_network`
- **Profiles:** `monitoring`, `prometheus`
- **Labels:**
  - `com.example.description`: "Container using Prometheus engine"
  - `com.example.department`: "BeeGis"

### Alertmanager

**Description:** Alertmanager handles alerts sent by Prometheus.

- **Image:** `prom/alertmanager:latest`
- **Ports:** `9093`
- **Volumes:** `${ALERTMANAGER_SOURCE_DIRECTORY}/alertmanager.yml:/etc/alertmanager/alertmanager.yml`
- **Networks:** `beegis_monitoring_network`
- **Profiles:** `monitoring`, `alertmanager`
- **Labels:**
  - `com.example.description`: "Container using Alertmanager engine"
  - `com.example.department`: "BeeGis"

### Tempo

**Description:** Tempo is used for distributed tracing.

- **Image:** `grafana/tempo:2.4.1`
- **Command:**
  - `--target=all`
  - `--storage.trace.backend=local`
  - `--storage.trace.local.path=/var/tempo`
  - `--auth.enabled=false`
- **Ports:** `4317`, `4318`
- **Depends_on:** `loki`
- **Networks:** `beegis_monitoring_network`, `beegis_public_network`
- **Profiles:** `monitoring`, `tempo`
- **Labels:**
  - `com.example.description`: "Container using Tempo engine"
  - `com.example.department`: "BeeGis"

### Grafana

**Description:** Grafana is used for visualizing metrics and logs.

- **Image:** `grafana/grafana:10.4.2`
- **Environment:**
  - `GF_AUTH_ANONYMOUS_ENABLED=true`
  - `GF_AUTH_ANONYMOUS_ORG_ROLE=Admin`
  - `GF_INSTALL_PLUGINS=timomyl-breadcrumb-panel,natel-discrete-panel`
- **Ports:** `3000`
- **Volumes:**
  - `${GRAFANA_SOURCE_DIRECTORY}:/etc/grafana/provisioning/datasources`
  - `${GRAFANA_SOURCE_DIRECTORY}/dashboards.yaml:/etc/grafana/provisioning/dashboards/dashboards.yaml`
  - `${GRAFANA_SOURCE_DIRECTORY}/dashboards:/etc/grafana/dashboards`
- **Depends_on:** `loki`, `prometheus`
- **Networks:** `beegis_monitoring_network`
- **Profiles:** `monitoring`, `grafana`
- **Labels:**
  - `com.example.description`: "Container using Grafana engine"
  - `com.example.department`: "BeeGis"

### MongoDB Exporter

**Description:** MongoDB Exporter collects metrics from MongoDB.

- **Image:** `percona/mongodb_exporter:0.40`
- **Ports:** `9216`
- **Environment:**
  - `MONGODB_URI="mongodb://jag:beem_project@beem-mongodb:27017/admin"`
  - `COLLECT_DATABASES=true`
  - `COLLECT_REPLICASET=true`
  - `COLLECT_TOPMETRICS=true`
- **Command:**
  - `--collect-all`
  - `--collector.profile`
  - `--log.level=info`
  - `--compatible-mode`
- **Networks:** `beegis_monitoring_network`
- **Profiles:** `monitoring`, `mongodb-exporter`
- **Labels:**
  - `com.example.description`: "Container using MongoDB Exporter engine"
  - `com.example.department`: "BeeGis"

### Postgres Exporter

**Description:** Postgres Exporter collects metrics from PostgreSQL.

- **Image:** `wrouesnel/postgres_exporter`
- **Ports:** `9187`
- **Volumes:** `${POSTGRES_EXPORTER_SOURCE_DIRECTORY}/conf:/docker-entrypoint-initdb.d`
- **Networks:** `beegis_monitoring_network`
- **Profiles:** `monitoring`, `postgres-exporter`
- **Labels:**
  - `com.example.description`: "Container using Postgres Exporter engine"
  - `com.example.department`: "BeeGis"

### Redis Exporter

**Description:** Redis Exporter collects metrics from Redis.

- **Image:** `oliver006/redis_exporter:latest`
- **Ports:** `9121`
- **Environment:**
  - `REDIS_ADDR=beem-redis:6379`
- **Networks:** `beegis_monitoring_network`
- **Profiles:** `monitoring`, `redis-exporter`
- **Labels:**
  - `com.example.description`: "Container using Redis Exporter engine"
  - `com.example.department`: "BeeGis"

### StatsD Exporter

**Description:** StatsD Exporter converts StatsD metrics to Prometheus metrics.

- **Image:** `prom/statsd-exporter`
- **Ports:** `9102`, `8125/udp`
- **Volumes:** `${STATSD_EXPORTER_SOURCE_DIRECTORY}/conf/statsd_mapping.yml:/tmp/statsd_mapping.yml`
- **Command:**
  - `--statsd.mapping-config=/tmp/statsd_mapping.yml`
  - `--statsd.listen-udp=:8125`
  - `--web.listen-address=:9102`
- **Networks:** `beegis_monitoring_network`, `beegis_airflow_network`
- **Profiles:** `monitoring`, `statsd-exporter`
- **Labels:**
  - `com.example.description`: "Container using StatsD Exporter engine"
  - `com.example.department`: "BeeGis"

### Node Exporter

**Description:** Node Exporter collects metrics from the system nodes (servers).

- **Image:** `prom/node-exporter`
- **Ports:** `9100`
- **Networks:** `beegis_monitoring_network`
- **Profiles:** `monitoring`, `node-exporter`
- **Labels:**
  - `com.example.description`: "Container using Node Exporter engine"
  - `com.example.department`: "BeeGis"

### cAdvisor

**Description:** cAdvisor collects metrics from Docker containers.

- **Image:** `gcr.io/cadvisor/cadvisor:v0.44.0`
- **Ports:** `8081` (host port changed from `8080` to `8081`)
- **Volumes:**
  - `/:/rootfs:ro`
  - `/var/run:/var/run:ro`
  - `/sys:/sys:ro`
  - `/var/lib/docker/:/var/lib/docker:ro`
- **Networks:** `beegis_monitoring_network`
- **Profiles:** `monitoring`, `cadvisor`
- **Labels:**
  - `com.example.description`: "Container using cAdvisor engine"
  - `com.example.department`: "BeeGis"

## Conclusion

This documentation provides an overview of the monitoring services used in your system, their roles, and their configurations. You can add it to your documentation to help developers and administrators understand and manage your monitoring architecture.
