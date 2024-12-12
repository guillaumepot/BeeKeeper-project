#!/bin/bash

# Common functions
prerequisites_check () {
  if [ "$1" = "1" ]; then
    if [ "$MONGODB_SETUP" = "True" ] && [ "$POSTGRES_SETUP" = "True" ] && [ "$API_SETUP" = "True" ] && [ "$AIRFLOW_SETUP" = "True" ]; then
      return 0
    else
      return_prerequisite_error
    fi
  elif [ "$1" = "2" ] || [ "$1" = "3" ]; then
    if [ "$MONGODB_SETUP" = "True" ] && [ "$POSTGRES_SETUP" = "True" ] && [ "$API_SETUP" = "True" ]; then
      return 0
    else
      return_prerequisite_error
    fi
  elif [ "$1" = "4" ]; then
    if [ "$AIRFLOW_SETUP" = "True" ]; then
      return 0
    else
      return_prerequisite_error
    fi
  else
    echo "An error occurred while checking prerequisites, exiting..."
    exit 1
  fi
}




### SCRIPT STARTS HERE ###

# Check if common.env exists
if [ ! -f common.env ]; then
  echo "common.env file not found, please generate it using init_services.sh"
  echo "Exiting.."
  exit 1
else
  # Get common env variables
  export $(grep -v '^#' common.env | xargs)
fi

echo "Set Default admin user in the postgres database ? (no recommended un production)"
echo "1. YES"
echo "2. NO"
read -p "Enter your choice (1/2) :" default_postgres_user_creation_choice

case $default_postgres_user_creation_choice in
  1)
    echo "Default user will be set in the Postgres 'users' database"
    ;;
  2)
    echo "Skipping default user setup"
    ;;
  *)
    echo "Invalid choice, exiting.."
    exit 1
    ;;
esac



echo "Choose services to start:"
echo "1. All services (include API, Databases, UI, Airflow, MLflow tracking server, Monitoring)"
echo "2. API & Database services (no UI)"
echo "3. Beegis services (API, Databases & UI)"
echo "4. Airflow services only (no API, no databases, no UI)"
echo "5. Mlflow Tracking server only (no API, no databases, no UI, no Airflow)"
read -p "Enter your choice (1/2/3/4) :" service_choice


case $service_choice in
  1)
    echo "Starting all services"
    profiles="api,database,beegis,airflow,mlflow,monitoring"
    echo "How many airflow workers do you want to start?"
    read -p "Enter the number of workers: " worker_count
    ;;
  2)
    echo "Starting API & Database services"
    profiles="api,database"
    ;;
  3)
    echo "Starting all Beegis services"
    profiles="api,database,beegis"
    ;;
  4)
    echo "Starting Airflow services"
    profiles="airflow"
    echo "How many airflow workers do you want to start?"
    read -p "Enter the number of workers: " worker_count
    ;;
  5)
    echo "Starting MLflow Tracking server"
    profiles="mlflow"
    ;;
  *)
    echo "Invalid choice, exiting.."
    exit 1
    ;;
esac

# Log-in to gitlab container registry to download image if necessary
echo "$REGISTRY_PASSWORD" | docker login "$GITLAB_REGISTRY_URL" -u "$REGISTRY_USERNAME" --password-stdin



# Start services
IFS=',' read -r -a profile_array <<< "$profiles"
for profile in "${profile_array[@]}"; do
  if [ "$profile" = "airflow" ]; then
    docker compose --profile "$profile" up -d --scale airflow-worker="$worker_count"
    continue
  else 
    docker compose --profile "$profile" up -d
  fi
done



sleep 15



if [ "$default_postgres_user_creation_choice" = "1" ]; then
  echo "Writing verified user with role = 3 (admin) in the Postgres 'users' database.."

  # Register user in the database via API
  curl -X 'POST' \
    'http://localhost:8000/register' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "username": "jagjag",
    "password": {
      "password": "Beem_project8!"
    },
    "email": "user@example.com"
  }'

  # Enable user verification and set role as admin in the database
  docker exec -i postgres_beem psql -U jag -d users -c "UPDATE users SET role = 3, verified = true WHERE username = 'jagjag';"

  # Get IP v4
  host_ip=$(hostname -I | awk '{print $1}')

  echo "API DOC: $host_ip:8000/docs"
  echo "User test credentials for API auth: jagjag | Beem_project8!"
fi


echo "Deployment done, services are ready to use."
echo "To stop the services, use the following script: stop_containers.sh"
