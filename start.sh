#!/bin/bash
set -e  
set -x  
echo "Current working directory: $(pwd)"

echo "Creating alembic/versions directory..."
mkdir -p alembic/versions

ls -l alembic
ls -l alembic/versions


echo "Running alembic upgrade..."

alembic revision --autogenerate -m "initial migration"
alembic upgrade head

echo "Starting the application..."
uvicorn src.app.backend.main:app --host 0.0.0.0 --port 8000 --reload
