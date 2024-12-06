#!/bin/bash

set -e

while ! nc -z ${POSTGRES_SERVER} ${POSTGRES_PORT}; do
  echo "Waiting for postgres to start..."
  sleep 3
done
echo "Postgres started"

alembic upgrade head

python3 ./main.py
