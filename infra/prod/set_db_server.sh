#!/bin/bash

export $(cat .env | xargs)

DB_IMAGE=postgres:13-alpine
docker pull $DB_IMAGE
docker run --name postgres -d \
  --env-file .env \
  -p 5432:5432 \
  -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data \
  $DB_IMAGE
