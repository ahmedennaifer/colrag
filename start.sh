#!/bin/bash


until nc -z db 5432; do
  echo "Waiting for the database..."
  sleep 1
done


alembic upgrade head

uvicorn src.app.backend.main:app --host 0.0.0.0 --port 8000
