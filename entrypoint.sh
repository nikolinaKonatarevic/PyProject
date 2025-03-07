#!/bin/sh

# Wait for the database to be ready
echo "Waiting for the database to be available..."

while ! nc -z db 5432 ; do
  sleep 0.1
done

echo "Database is up - executing command"

echo "Running migrations..."
alembic upgrade head
echo "Migrations complete"


# Start the FastAPI server
if [ "${TEST}" = "True" ]; then
    pytest
else
    uvicorn src.main:app --host 0.0.0.0
fi

exec "$@"
