#!/bin/sh

postgres_ready() {
  python <<END
import sys

import psycopg2

try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${DB_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError as e:
    print(e)
    sys.exit(-1)
sys.exit(0)

END
}

until postgres_ready; do
  echo >&2 "Waiting for PostgreSQL..."
  sleep 1
done

echo >&2 "PostgreSQL is availalbe"

exec "$@"
