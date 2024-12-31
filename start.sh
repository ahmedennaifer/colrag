#!/bin/bash

set -e
set -x


source .env

echo "Current working directory: $(pwd)"


echo "Creating alembic/versions directory..."
mkdir -p alembic/versions
ls -l alembic
ls -l alembic/versions


echo "Initializing fresh Alembic setup..."

rm -f alembic/versions/*


PGPASSWORD=${DB_PASSWORD} psql -h ${DB_HOST} -U ${DB_USER} -d ${DB_NAME} -c "DROP TABLE IF EXISTS alembic_version;"


echo "Creating new initial migration..."
alembic revision --autogenerate -m "fresh_start"


echo "Applying migration..."
alembic upgrade head

echo "Starting the application..."
uvicorn src.app.backend.main:app --host 0.0.0.0 --port 8000 --reload
