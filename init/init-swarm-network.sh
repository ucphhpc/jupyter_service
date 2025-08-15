#!/bin/bash
SERVICE_NETWORK_NAME=$1
SERVICE_NETWORK_RANGE=$2

if [[ -z ${SERVICE_NETWORK_NAME} ]]; then
    SERVICE_NETWORK_NAME=jupyter-service_default
fi

if [[ -z ${SERVICE_NETWORK_RANGE} ]]; then
    SERVICE_NETWORK_RANGE=10.1.0.0/16
fi

docker network create --attachable --driver overlay --subnet=${SERVICE_NETWORK_RANGE} ${SERVICE_NETWORK_NAME}