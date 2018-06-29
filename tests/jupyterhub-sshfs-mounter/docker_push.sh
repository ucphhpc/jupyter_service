#!/bin/bash
docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
docker push "$DOCKER_USERNAME"/ssh-mount-dummy:latest
