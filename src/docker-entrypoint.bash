#!/bin/bash

set -e

echo "Waiting for postgres to start..."
while ! nc -z ${POSTGRES_SERVER} ${POSTGRES_PORT}; do
  echo "Retrying to $POSTGRES_SERVER:$POSTGRES_PORT"
  sleep 3
done
echo "Postgres started"

alembic upgrade head

exec python3 ./main.py
