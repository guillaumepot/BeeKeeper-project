#!/bin/bash

ROOT_DIRECTORY=".."
COMMON_DOT_ENV_FILEPATH="$ROOT_DIRECTORY/utils/common.env"

source script_functions/write_default_common_env.sh
source script_functions/write_default_postgres_env.sh
source script_functions/write_default_mongodb_env.sh
source script_functions/write_default_airflow_env.sh
source script_functions/write_default_api_env.sh
source script_functions/write_default_beegis_env.sh
source script_functions/write_default_mlflow_env.sh
source script_functions/write_default_alertmanager_env.sh
source script_functions/write_default_prometheus_env.sh
source script_functions/write_default_grafana_env.sh
source script_functions/write_default_loki_env.sh
source script_functions/write_default_mongodb_exporter_env.sh
source script_functions/write_default_postgres_exporter_env.sh
source script_functions/write_default_prometheus_env.sh
source script_functions/write_default_promtail_env.sh
source script_functions/write_default_statsd_env.sh
source script_functions/create_docker_networks.sh
source script_functions/remove_docker_networks.sh
source script_functions/flush_services_configuration.sh


if [ -f "$COMMON_DOT_ENV_FILEPATH" ]; then
    echo "File $COMMON_DOT_ENV_FILEPATH already exists."
    echo "Flush & restart services configuration ? (y/n)"
    read -r flush_choice

    case $flush_choice in
        [yY]*)
            echo "Flushing services configuration..."
            export $(grep -v '^#' "$COMMON_DOT_ENV_FILEPATH" | xargs)
            flush_services_configuration
            echo "Services configuration flushed."
            exit 0
            ;;
        [nN]*)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid input..."
            exit 1
            ;;
    esac
else
    write_default_common_env_configuration
    export $(grep -v '^#' "$COMMON_DOT_ENV_FILEPATH" | xargs)
    mkdir -p "$SECRETS_DIRECTORY/api"
    mkdir -p "$SECRETS_DIRECTORY/postgres"
    mkdir -p "$SECRETS_DIRECTORY/mongodb"
    mkdir -p "$SECRETS_DIRECTORY/airflow"
    mkdir -p "$SECRETS_DIRECTORY/beegis"
    mkdir -p "$SECRETS_DIRECTORY/alertmanager"
    mkdir -p "$SECRETS_DIRECTORY/prometheus"
    mkdir -p "$SECRETS_DIRECTORY/grafana"
    mkdir -p "$SECRETS_DIRECTORY/loki"
    mkdir -p "$SECRETS_DIRECTORY/promtail"
    mkdir -p "$SECRETS_DIRECTORY/postgres-exporter"
    mkdir -p "$POSTGRES_DATA_DIRECTORY"
    mkdir -p "$MONGODB_DATA_DIRECTORY"
    mkdir -p "$AIRFLOW_DATA_DIRECTORY"
    mkdir -p "$MLFLOW_DATA_DIRECTORY"
    mkdir -p "$GRAFANA_DATA_DIRECTORY"
    mkdir -p "$GRAFANA_DATA_DIRECTORY/provisioning/datasources"
    mkdir -p "$GRAFANA_DATA_DIRECTORY/provisioning/dashboards"
    mkdir -p "$LOKI_DATA_DIRECTORY"
    mkdir -p "$PROMETHEUS_DATA_DIRECTORY"
    mkdir -p "$PROMTAIL_DATA_DIRECTORY"
    mkdir -p "$DATA_RAW_DIRECTORY"
    mkdir -p "$DATA_PROCESSING_DIRECTORY"
    mkdir -p "$DATA_ARCHIVES_DIRECTORY"
    mkdir -p "$DATA_CLEANED_DIRECTORY"
    mkdir -p "$SEGMENTATION_MODELS_DIRECTORY"
    mkdir -p "$LOGS_DIRECTORY"
    write_default_postgres_env_configuration
    write_default_mongodb_env_configuration
    write_default_airflow_env_configuration
    write_default_api_env_configuration
    write_default_beegis_env_configuration
    write_default_mlflow_env_configuration
    write_default_prometheus_env_configuration
    write_default_alertmanager_env_configuration
    write_default_grafana_env_configuration
    write_default_statsd_env_configuration
    write_default_mongodb_exporter_env_configuration
    write_default_postgres_exporter_env_configuration
    create_docker_networks
fi