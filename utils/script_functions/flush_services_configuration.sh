#!/bin/bash

flush_services_configuration() {
    echo "Flushing configuration files..."
    echo "All .env files will be deleted."
    read -p "Press enter to continue, or CTRL+C to cancel."

    echo "Deleting all .env files:"
    echo "rm -rf $API_ENV_FILEPATH"
    echo "rm -rf $POSTGRES_ENV_FILEPATH"
    echo "rm -rf $MONGODB_ENV_FILEPATH"
    echo "rm -rf $AIRFLOW_ENV_FILEPATH"
    echo "rm -rf $BEEGIS_ENV_FILEPATH"
    echo "rm -rf $ALERTMANAGER_ENV_FILEPATH"
    echo "rm -rf $GRAFANA_ENV_FILEPATH"
    echo "rm -rf $MONGODB_EXPORTER_ENV_FILEPATH"
    echo "rm -rf $LOKI_ENV_FILEPATH"
    echo "rm -rf $POSTGRES_EXPORTER_ENV_FILEPATH"
    echo "rm -rf $PROMETHEUS_ENV_FILEPATH"
    echo "rm -rf $PROMTAIL_ENV_FILEPATH"
    echo "rm -rf $COMMON_DOT_ENV_FILEPATH"

    echo "Deleting secrets"
    echo "rm -rf $SECRETS_DIRECTORY"

    rm -rf "$API_ENV_FILEPATH"
    rm -rf "$POSTGRES_ENV_FILEPATH"
    rm -rf "$MONGODB_ENV_FILEPATH"
    rm -rf "$AIRFLOW_ENV_FILEPATH"
    rm -rf "$BEEGIS_ENV_FILEPATH"
    rm -rf "$COMMON_DOT_ENV_FILEPATH"
    rm -rf "$ALERTMANAGER_ENV_FILEPATH"
    rm -rf "$GRAFANA_ENV_FILEPATH"
    rm -rf "$LOKI_ENV_FILEPATH"
    rm -rf "$MONGODB_EXPORTER_ENV_FILEPATH"
    rm -rf "$POSTGRES_EXPORTER_ENV_FILEPATH"
    rm -rf "$PROMETHEUS_ENV_FILEPATH"
    rm -rf "$PROMTAIL_ENV_FILEPATH"
    rm -rf "$POSTGRES_EXPORTER_ENV_FILEPATH"
    rm -rf "$SECRETS_DIRECTORY"

    echo "Removing docker networks..."
    remove_docker_networks

    echo "Configuration files flushed."
    echo "Database data will be kept, please delete manually if needed."
    echo "Path to your database data: $DATABASES_DATA_DIRECTORY"
}