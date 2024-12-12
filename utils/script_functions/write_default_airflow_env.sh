#!/bin/bash

write_default_airflow_env_configuration () {
    echo "Writing Airflow default configuration..."
    echo "Default Airflow configuration will be written here: $AIRFLOW_ENV_FILEPATH"
    echo "Airflow secrets will be written here: $AIRFLOW_SECRETS_DIRECTORY"
    echo -e "\n"

    cat <<EOF | tee "$AIRFLOW_ENV_FILEPATH"
# Airflow webserver configuration
_AIRFLOW_WWW_USER_USERNAME=jag
AIRFLOW__CORE__EXECUTOR=CeleryExecutor
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@airflow_postgres/airflow
AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@airflow_postgres/airflow
AIRFLOW__CELERY__BROKER_URL=redis://:@beem_redis:6379/0
AIRFLOW__CORE__FERNET_KEY=''
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION='true'
AIRFLOW__CORE__LOAD_EXAMPLES='false'
AIRFLOW__API__AUTH_BACKENDS='airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session'
AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK='true'
AIRFLOW_CONN_FS_DEFAULT='fs://:@/opt/airflow/storage/raw_data'

# Airflow init configuration
_AIRFLOW_DB_MIGRATE='true'
_AIRFLOW_WWW_USER_CREATE='true'
_AIRFLOW_WWW_USER_PASSWORD_CMD="cat /run/secrets/airflow_webserver_password"
_PIP_ADDITIONAL_REQUIREMENTS=''

# Airflow DAGs schedulers
ETL_PIPELINE_SCHEDULER='0 */12 * * *'
SEGMENTED_PIPELINE_SCHEDULER=None
ML_PIPELINE_SCHEDULER=None

# Tasks misc configurations
API_URL="http://178.16.130.232:8000"
API_VERSION=v1
ROUTE_CARTO_SUFIX=carto
EOF

    echo -e "\n"
    echo "Writing Airflow secrets configuration"
    echo "beem_project" > "$AIRFLOW_SECRETS_DIRECTORY/_AIRFLOW_WWW_USER_PASSWORD"

    chmod 644 "$AIRFLOW_SECRETS_DIRECTORY/_AIRFLOW_WWW_USER_PASSWORD"

    echo "Airflow secrets default configuration written here: $AIRFLOW_SECRETS_DIRECTORY"
    echo "Please change default values for security reasons."

    sed -i 's/AIRFLOW_SETUP=False/AIRFLOW_SETUP=True/' $COMMON_DOT_ENV_FILEPATH
}