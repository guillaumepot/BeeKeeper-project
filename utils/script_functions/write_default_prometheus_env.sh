#!/bin/bash

write_default_prometheus_env_configuration () {

    echo "Writing Prometheus default configuration..."
    echo "Default Prometheus configuration will be written here: $PROMETHEUS_ENV_FILEPATH"
    echo "Prometheus secrets will be written here: $PROMETHEUS_SECRETS_DIRECTORY"
    echo -e "\n"

    cat <<EOF | tee "$PROMETHEUS_ENV_FILEPATH"
# Prometheus database configuration
EOF

    echo -e "\n"
    echo "Writing PROMETHEUS secrets configuration"
    echo "beem_project" > "$PROMETHEUS_SECRETS_DIRECTORY/PROMETHEUS_PASSWORD"

    chmod 644 "$PROMETHEUS_SECRETS_DIRECTORY/PROMETHEUS_PASSWORD"

    echo "Prometheus secrets default configuration written here: $PROMETHEUS_SECRETS_DIRECTORY"
    echo "Please change default values for security reasons."

    sed -i '' 's/PROMETHEUS_SETUP=False/PROMETHEUS_SETUP=True/' "$COMMON_DOT_ENV_FILEPATH"
}