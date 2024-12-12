#!/bin/bash

write_default_mongodb_env_configuration () {
    echo "Writing MongoDB default configuration..."
    echo "Default MongoDB configuration will be written here: $MONGODB_ENV_FILEPATH"
    echo "MongoDB secrets will be written here: $MONGODB_SECRETS_DIRECTORY"
    echo -e "\n"

    cat <<EOF | tee "$MONGODB_ENV_FILEPATH"
# MongoDB database configuration
MONGODB_DATABASE=data_user_beegis
MONGO_INITDB_ROOT_USERNAME=jag
EOF

    echo -e "\n"
    echo "Writing MONGODB secrets configuration"
    echo "beem_project" > "$MONGODB_SECRETS_DIRECTORY/MONGO_INITDB_ROOT_PASSWORD"

    chmod 644 "$MONGODB_SECRETS_DIRECTORY/MONGO_INITDB_ROOT_PASSWORD"

    echo "MongoDB secrets default configuration written here: $MONGODB_SECRETS_DIRECTORY"
    echo "Please change default values for security reasons."

    sed -i 's/MONGODB_SETUP=False/MONGODB_SETUP=True/' $COMMON_DOT_ENV_FILEPATH
}