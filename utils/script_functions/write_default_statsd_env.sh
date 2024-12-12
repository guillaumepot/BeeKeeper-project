#!/bin/bash

write_default_statsd_env_configuration () {

    echo "Writing StatsD default configuration..."
    echo "Default StatsD configuration will be written here: $COMMON_DOT_ENV_FILEPATH"
    echo -e "\n"

    cat <<EOF | tee -a "$COMMON_DOT_ENV_FILEPATH"
# StatsD configuration
STATSD_HOST=statsd-exporter
STATSD_PORT=9125
METRICS_ON=true
EOF

    echo "StatsD default configuration written."
}