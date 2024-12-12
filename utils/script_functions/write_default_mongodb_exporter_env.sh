#!/bin/bash

write_default_mongodb_exporter_env_configuration () {

    echo "Writing MongoDB Exporter default configuration..."
    echo "Default MongoDB Exporter configuration will be written here: $MONGODB_EXPORTER_ENV_FILEPATH"
    echo -e "\n"

    cat <<EOF | tee "$MONGODB_EXPORTER_ENV_FILEPATH"
# MongoDB Exporter configuration
MONGODB_URI="mongodb://jag:beem_project@beem-mongodb:27017"
EOF

    echo -e "\n"
 

    sed -i '' 's/MONGODB_EXPORTER_SETUP=False/MONGODB_EXPORTER_SETUP=True/' "$COMMON_DOT_ENV_FILEPATH"
}