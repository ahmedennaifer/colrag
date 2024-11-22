#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status
set -x  # Print commands and their arguments as they are executed

# Debugging statements
echo "Current working directory: $(pwd)"
ls -l

until nc -z db 5432; do
  echo "Waiting for the database..."
  sleep 1
done

# Create the alembic/versions directory
echo "Creating alembic/versions directory..."
mkdir -p alembic/versions

# List contents to verify
ls -l alembic
ls -l alembic/versions

echo "Running alembic revision..."
alembic revision --autogenerate -m "Initial migration"

echo "Running alembic upgrade..."
alembic upgrade head

echo "Starting the application..."
uvicorn src.app.backend.main:app --host 0.0.0.0 --port 8000 --reload
