#!/bin/bash

export $(grep -v '^#' common.env | xargs)
docker compose --profile airflow down
docker compose --profile mlflow down
docker compose --profile api down
docker compose --profile database down
docker compose --profile beegis down
docker compose --profile monitoring down