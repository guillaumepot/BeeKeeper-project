#!/bin/bash

write_default_api_env_configuration () {
    echo "Writing API default configuration..."
    echo "Default API configuration will be written here: $API_ENV_FILEPATH"
    echo "API secrets will be written here: $API_SECRETS_DIRECTORY"
    echo -e "\n"

    cat <<EOF | tee "$API_ENV_FILEPATH"
# Debug Mode
DEBUG=True

# Logging
LOGGER=False
LOG_FILE_PATH=/app/logs/api.log

# Route limiter
LIMITER_TYPE=user  # Change to ip if needed
DEFAULT_LIMITS_FOR_LIMITER=60/minute
STATUS_LIMIT=5/minute
DATABASE_CHECK_LIMIT=5/minute
TEST_LIMIT=10/minute
INSERT_INFOS_LIMIT=3/minute
UPDATE_INFOS_LIMIT=3/minute
PASSWORD_UPDATE_LIMIT=1/minute
USER_LOCATIONS_LIMIT=15/minute
WEATHER_LIMIT=15/minute
CARTO_LIMIT=60/minute

# Hash & encryption algorithms & JWT
HASH_ALGORITHM=argon2
ENCODING_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRATION_IN_MINUTES=60

# Database connections
POSTGRES_HOST=postgres_beem
POSTGRES_PORT=5432
POSTGRES_API_USER=jag
CARTO_DATABASE=dbcarto
USER_DATABASE=users
MONGODB_HOST=mongodb_beem
MONGODB_PORT=27017
MONGODB_API_USER=jag
MONGODB_DATABASE=data_user_beegis
MONGODB_LOCATION_COLLECTION_NAME=locations
MONGODB_HIVES_COLLECTION_NAME=hives
REDIS_HOST=beem-redis
REDIS_PORT=6379

# Cartographic data types
AVAILABLE_CARTO_DATA_TYPES=rpg,clc,forest_v2,c1l

EOF

    echo -e "\n"
    echo "Writing API secrets configuration"
    echo "BEEMPROJECT2024SK" > "$API_SECRETS_DIRECTORY/JWT_SECRET_KEY"
    echo "beem_project" > "$API_SECRETS_DIRECTORY/POSTGRES_API_PASSWORD"
    echo "beem_project" > "$API_SECRETS_DIRECTORY/MONGODB_API_PASSWORD"

    chmod 644 "$API_SECRETS_DIRECTORY/JWT_SECRET_KEY"
    chmod 644 "$API_SECRETS_DIRECTORY/POSTGRES_API_PASSWORD"
    chmod 644 "$API_SECRETS_DIRECTORY/MONGODB_API_PASSWORD"

    echo "API secrets default configuration written here: $API_SECRETS_DIRECTORY"
    echo "Please change default values for security reasons."

    sed -i 's/API_SETUP=False/API_SETUP=True/' $COMMON_DOT_ENV_FILEPATH

    echo -e "\n"
    echo -e "\n"
}