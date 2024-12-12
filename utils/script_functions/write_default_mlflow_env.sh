#!/bin/bash

write_default_mlflow_env_configuration () {
    echo "Writing Mlflow default configuration..."
    echo "Default Mlflow configuration will be written here: $MLFLOW_ENV_FILEPATH"
    echo -e "\n"

    cat <<EOF | tee "$MLFLOW_ENV_FILEPATH"
# MLFLOW configuration
# HOST & PORT for tracking server
MLFLOW_HOST=0.0.0.0
MLFLOW_PORT=8002

# Tracking URI (where the tracking server find the data)
MLFLOW_TRACKING_URI=/app/storage
EOF

    sed -i 's/MLFLOW_SETUP=False/MLFLOW_SETUP=True/' $COMMON_DOT_ENV_FILEPATH
}