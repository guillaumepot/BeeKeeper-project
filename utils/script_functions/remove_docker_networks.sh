#!/bin/bash

remove_docker_networks () {
    docker network rm beegis_critical_data_transit_network
    docker network rm beegis_public_network
    docker network rm beegis_airflow_network
    docker network rm beegis_monitoring_network
}