#!/bin/bash

write_default_postgres_exporter_env_configuration () {

    echo "Writing Postgres Exporter default configuration..."
    echo "Default Postgres Exporter configuration will be written here: $POSTGRES_EXPORTER_ENV_FILEPATH"
    echo -e "\n"

    cat <<EOF | tee "$POSTGRES_EXPORTER_ENV_FILEPATH"
# Postgres database configuration
POSTGRES_HOST=postgres_beem
POSTGRES_PORT=5432
POSTGRES_API_USER=jag
CARTO_DATABASE=dbcarto
POSTGRES_EXPORTER_PORT=9187
USER_DATABASE=users
DATA_SOURCE_NAME=postgresql://jag:beem_project@beem-postgres:5432/dbcarto?sslmode=disable
EOF

    echo -e "\n"
    echo "Writing POSTGRES EXPORTER secrets configuration"
    echo "beem_project" > "$POSTGRES_EXPORTER_SECRETS_DIRECTORY/POSTGRES_EXPORTER_PASSWORD"

    chmod 644 "$POSTGRES_EXPORTER_SECRETS_DIRECTORY/POSTGRES_EXPORTER_PASSWORD"

    echo "Postgres Exporter secrets default configuration written here: $POSTGRES_EXPORTER_SECRETS_DIRECTORY"
    echo "Please change default values for security reasons."

    sed -i '' 's/POSTGRES_EXPORTER_SETUP=False/POSTGRES_EXPORTER_SETUP=True/' "$COMMON_DOT_ENV_FILEPATH"
}