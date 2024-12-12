#!/bin/bash

write_default_common_env_configuration () {
    echo "common.env file does not exist."
    echo "Writing default configuration..."
    echo "Default configuration includes all services configuration files and the common.env file."
    echo -e "\n"
    echo "The following default configurations will be written:"
    echo -e "\n"

    cat <<EOF | tee "$COMMON_DOT_ENV_FILEPATH"
# Services setup information
API_SETUP=False
POSTGRES_SETUP=False
MONGODB_SETUP=False
AIRFLOW_SETUP=False
BEEGIS_SETUP=False
MLFLOW_SETUP=False
ALERTMANAGER_SETUP=False
PROMETHEUS_SETUP=False
GRAFANA_SETUP=False
LOKI_SETUP=False
POSTGRES_EXPORTER_SETUP=False
MONGODB_EXPORTER_SETUP=False

# Gitlab workspace registry
GITLAB_REGISTRY_URL="registry.gitlab.com/beem-project-de/beem"
REGISTRY_USERNAME="gitlab+deploy-token-5386668"
REGISTRY_PASSWORD="gldt-3yg1FwDsu7yiqpCQMEwg"

# Data filepaths
DATA_DIRECTORY=../data
DATA_RAW_DIRECTORY=../data/raw
DATA_PROCESSING_DIRECTORY=../data/processing
DATA_ARCHIVES_DIRECTORY=../data/archives
DATA_CLEANED_DIRECTORY=../data/cleaned
SEGMENTATION_MODELS_DIRECTORY=../data/segmentation_models
DATABASES_DATA_DIRECTORY=../data/databases
POSTGRES_DATA_DIRECTORY=../data/databases/postgres_data
MONGODB_DATA_DIRECTORY=../data/databases/mongodb_data
AIRFLOW_DATA_DIRECTORY=../data/databases/airflow_data
MLFLOW_DATA_DIRECTORY=../data/mlflow_data
LOKI_DATA_DIRECTORY=../data/storage/loki

# Logs filepaths
LOGS_DIRECTORY=../logs

# Sources filepaths
API_SOURCE_DIRECTORY=../src/api
API_ENV_FILEPATH=../src/api/.env
POSTGRES_SOURCE_DIRECTORY=../src/postgres
POSTGRES_ENV_FILEPATH=../src/postgres/.env
MONGODB_SOURCE_DIRECTORY=../src/mongodb
MONGODB_ENV_FILEPATH=../src/mongodb/.env
REDIS_SOURCE_DIRECTORY=../src/redis
AIRFLOW_SOURCE_DIRECTORY=../src/airflow
AIRFLOW_ENV_FILEPATH=../src/airflow/.env
MLFLOW_SOURCE_DIRECTORY=../src/mlflow
MLFLOW_ENV_FILEPATH=../src/mlflow/.env
BEEGIS_SOURCE_DIRECTORY=../src/beegis
BEEGIS_ENV_FILEPATH=../src/beegis/.env
ALERTMANAGER_SOURCE_DIRECTORY=../src/alertmanager
ALERTMANAGER_ENV_FILEPATH=../src/alertmanager/.env
GRAFANA_SOURCE_DIRECTORY=../src/grafana
GRAFANA_ENV_FILEPATH=../src/grafana/.env
MONGODB_EXPORTER_SOURCE_DIRECTORY=../src/mongodb-exporter
MONGODB_EXPORTER_ENV_FILEPATH=../src/mongodb-exporter/.env
LOKI_SOURCE_DIRECTORY=../src/loki
LOKI_ENV_FILEPATH=../src/loki/.env
POSTGRES_EXPORTER_SOURCE_DIRECTORY=../src/postgres-exporter
POSTGRES_EXPORTER_ENV_FILEPATH=../src/postgres-exporter/.env
PROMETHEUS_SOURCE_DIRECTORY=../src/prometheus
PROMETHEUS_ENV_FILEPATH=../src/prometheus/.env
PROMTAIL_SOURCE_DIRECTORY=../src/promtail
PROMTAIL_ENV_FILEPATH=../src/promtail/.env
STATSD_EXPORTER_SOURCE_DIRECTORY=../src/statsd
STATSD_EXPORTER_ENV_FILEPATH=../src/statsd/.env

# Services METADATA
API_VERSION=v1
AIRFLOW_UID=$(id -u)

# Services Secrets filepaths
SECRETS_DIRECTORY=./secrets
API_SECRETS_DIRECTORY=./secrets/api
POSTGRES_SECRETS_DIRECTORY=./secrets/postgres
POSTGRES_EXPORTER_SECRETS_DIRECTORY=./secrets/postgres
MONGODB_SECRETS_DIRECTORY=./secrets/mongodb
AIRFLOW_SECRETS_DIRECTORY=./secrets/airflow
BEEGIS_SECRETS_DIRECTORY=./secrets/beegis
ALERTMANAGER_SECRETS_DIRECTORY=./secrets/alertmanager
GRAFANA_SECRETS_DIRECTORY=./secrets/grafana
LOKI_SECRETS_DIRECTORY=./secrets/loki
PROMETHEUS_SECRETS_DIRECTORY=./secrets/prometheus
PROMTAIL_SECRETS_DIRECTORY=./secrets/promtail
EOF

    echo -e "\n"
    echo -e "\n"
}