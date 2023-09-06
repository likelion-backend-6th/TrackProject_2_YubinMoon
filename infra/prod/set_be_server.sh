#!/bin/sh

export $(cat .env | xargs)

DOCKER_IMAGE=$NCR_REGISTRY/follow-app:latest

docker login -u $DOCKER_USER -p $DOCKER_PASSWORD $NCR_REGISTRY

docker run -d --rm --name follow-app \
  --env-file .env \
  -p 8000:8000 \
  $DOCKER_IMAGE \
  /start
