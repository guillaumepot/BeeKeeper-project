#!/bin/bash

write_default_beegis_env_configuration () {
    echo "Writing Beegis default configuration..."
    echo "Default Beegis configuration will be written here: $BEEGIS_ENV_FILEPATH"
    echo "Beegis secrets will be written here: $BEEGIS_SECRETS_DIRECTORY"
    echo -e "\n"

    cat <<EOF | tee "$BEEGIS_ENV_FILEPATH"
# API connection
API_HOST=beem_api
API_PORT=5000
UI_API_USER=jagjag
EOF

    echo -e "\n"
    echo "Writing API secrets configuration"
    echo "Beem_project8!" > "$BEEGIS_SECRETS_DIRECTORY/UI_API_PASSWORD"

    chmod 644 "$BEEGIS_SECRETS_DIRECTORY/UI_API_PASSWORD"

    echo "Beegis UI secrets default configuration written here: $BEEGIS_SECRETS_DIRECTORY"
    echo "Please change default values for security reasons."

    sed -i 's/BEEGIS_SETUP=False/BEEGIS_SETUP=True/' $COMMON_DOT_ENV_FILEPATH

    echo -e "\n"
    echo -e "\n"
}