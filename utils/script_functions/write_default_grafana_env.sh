#!/bin/bash

write_default_grafana_env_configuration () {

    echo "Writing Grafana default configuration..."
    echo "Default Grafana configuration will be written here: $GRAFANA_ENV_FILEPATH"
    echo "Grafana secrets will be written here: $GRAFANA_SECRETS_DIRECTORY"
    echo -e "\n"

    cat <<EOF | tee "$GRAFANA_ENV_FILEPATH"
# Grafana database configuration
EOF

    echo -e "\n"
    echo "Writing Grafana secrets configuration"
    echo "beem_project" > "$GRAFANA_SECRETS_DIRECTORY/GRAFANA_PASSWORD"

    chmod 644 "$GRAFANA_SECRETS_DIRECTORY/GRAFANA_PASSWORD"

    echo "AlertManager secrets default configuration written here: $GRAFANA_SECRETS_DIRECTORY"
    echo "Please change default values for security reasons."

    sed -i '' 's/GRAFANA_SETUP=False/GRAFANA_SETUP=True/' "$COMMON_DOT_ENV_FILEPATH"
}