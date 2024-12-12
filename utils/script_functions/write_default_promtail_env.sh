#!/bin/bash

write_default_promtail_env_configuration () {

    echo "Writing Promtail default configuration..."
    echo "Default Promtail configuration will be written here: $PROMTAIL_ENV_FILEPATH"
    echo "Promtail secrets will be written here: $PROMTAIL_SECRETS_DIRECTORY"
    echo -e "\n"

    cat <<EOF | tee "$PROMTAIL_ENV_FILEPATH"
    # Promtail database configuration
EOF

    echo -e "\n"
    echo "Writing Promtail secrets configuration"
    echo "beem_project" > "$PROMTAIL_SECRETS_DIRECTORY/PROMTAIL_PASSWORD"

    chmod 644 "$PROMTAIL_SECRETS_DIRECTORY/PROMTAIL_PASSWORD"

    echo "Promtail secrets default configuration written here: $PROMTAIL_SECRETS_DIRECTORY"
    echo "Please change default values for security reasons."

    sed -i '' 's/PROMTAIL_SETUP=False/PROMTAIL_SETUP=True/' "$COMMON_DOT_ENV_FILEPATH"
}