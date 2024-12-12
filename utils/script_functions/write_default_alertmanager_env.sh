#!/bin/bash

write_default_alertmanager_env_configuration () {

    echo "Writing AlertManager default configuration..."
    echo "Default AlertManager configuration will be written here: $ALERTMANAGER_ENV_FILEPATH"
    echo "AlertManager secrets will be written here: $ALERTMANAGER_SECRETS_DIRECTORY"
    echo -e "\n"

    cat <<EOF | tee "$ALERTMANAGER_ENV_FILEPATH"
# AlertManager database configuration
EOF

    echo -e "\n"
    echo "Writing AlertManager secrets configuration"
    echo "beem_project" > "$ALERTMANAGER_SECRETS_DIRECTORY/ALERTMANAGER_PASSWORD"

    chmod 644 "$ALERTMANAGER_SECRETS_DIRECTORY/ALERTMANAGER_PASSWORD"

    echo "AlertManager secrets default configuration written here: $ALERTMANAGER_SECRETS_DIRECTORY"
    echo "Please change default values for security reasons."

    sed -i '' 's/ALERTMANAGER_SETUP=False/ALERTMANAGER_SETUP=True/' "$COMMON_DOT_ENV_FILEPATH"
}