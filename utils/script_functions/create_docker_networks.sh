#!/bin/bash

create_docker_networks () {
    if ! docker network ls | grep -q "beegis_critical_data_transit_network"; then
    docker network create --driver bridge beegis_critical_data_transit_network
    fi

    # Check if the beegis_public_network exists
    if ! docker network ls | grep -q "beegis_public_network"; then
    docker network create --driver bridge beegis_public_network
    fi

    # Check if the beegis_airflow_network exists
    if ! docker network ls | grep -q "beegis_airflow_network"; then
    docker network create --driver bridge beegis_airflow_network
    fi

    # Check if the beegis_monitoring_network exists
    if ! docker network ls | grep -q "beegis_monitoring_network"; then
    docker network create --driver bridge beegis_monitoring_network
    fi
}