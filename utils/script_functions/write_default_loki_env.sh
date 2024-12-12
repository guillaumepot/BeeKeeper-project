#!/bin/bash

write_default_loki_env_configuration () {

    echo "Writing Loki default configuration..."
    echo "Default Loki configuration will be written here: $LOKI_ENV_FILEPATH"
    echo "Loki secrets will be written here: $LOKI_SECRETS_DIRECTORY"
    echo -e "\n"

    cat <<EOF | tee "$LOKI_ENV_FILEPATH"
# LOKI database configuration
EOF

    echo -e "\n"
    echo "Writing Loki secrets configuration"
    echo "beem_project" > "$LOKI_SECRETS_DIRECTORY/LOKI_PASSWORD"

    chmod 644 "$LOKI_SECRETS_DIRECTORY/LOKI_PASSWORD"

    echo "Loki secrets default configuration written here: $LOKI_SECRETS_DIRECTORY"
    echo "Please change default values for security reasons."

    sed -i '' 's/LOKI_SETUP=False/LOKI_SETUP=True/' "$COMMON_DOT_ENV_FILEPATH"
}

# Vérifier si le plugin loki est déjà installé
echo "Checking if loki plugin is already installed..."
docker plugin ls | grep loki

if [ $? -eq 0 ]; then
    echo "Loki plugin is already installed."
else
    # Installer le plugin loki
    echo "Installing loki plugin..."
    docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions

    # Vérifier si l'installation a réussi
    if [ $? -eq 0 ]; then
        echo "Loki plugin installed successfully."
    else
        echo "Failed to install loki plugin."
        exit 1
    fi
fi

# Vérifier que le plugin est installé
echo "Checking installed plugins..."
docker plugin ls | grep loki

# Vérifier si Docker a redémarré correctement
if [ $? -eq 0 ]; then
    echo "Docker restarted successfully."
else
    echo "Failed to restart Docker."
    exit 1
fi

# Vérifier que le plugin est installé
echo "Checking installed plugins..."
docker plugin ls | grep loki

if [ $? -eq 0 ]; then
    echo "Loki plugin is installed and ready to use."
else
    echo "Loki plugin is not found."
    exit 1
fi