#!/bin/bash

echo "=== AI SOC Backend Startup ==="
echo "Database URL: ${DATABASE_URL:0:50}..."

# Try to run migrations, but don't fail if they error
# (tables might already exist from create_all)
echo "Running database migrations..."
alembic upgrade head || echo "Migration warning (tables may already exist), continuing..."

echo "Starting server on port ${PORT:-8000}..."
exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
