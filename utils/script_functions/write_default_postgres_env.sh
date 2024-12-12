#!/bin/bash

write_default_postgres_env_configuration () {
    echo "Writing Postgres default configuration..."
    echo "Default Postgres configuration will be written here: $POSTGRES_ENV_FILEPATH"
    echo "Postgres secrets will be written here: $POSTGRES_SECRETS_DIRECTORY"
    echo -e "\n"

    cat <<EOF | tee "$POSTGRES_ENV_FILEPATH"
# Postgres database configuration
POSTGRES_DB=dbcarto
POSTGRES_USER=jag
EOF

    echo -e "\n"
    echo "Writing POSTGRES secrets configuration"
    echo "beem_project" > "$POSTGRES_SECRETS_DIRECTORY/POSTGRES_PASSWORD"

    chmod 644 "$POSTGRES_SECRETS_DIRECTORY/POSTGRES_PASSWORD"

    echo "Postgres secrets default configuration written here: $POSTGRES_SECRETS_DIRECTORY"
    echo "Please change default values for security reasons."

    sed -i 's/POSTGRES_SETUP=False/POSTGRES_SETUP=True/' $COMMON_DOT_ENV_FILEPATH
}