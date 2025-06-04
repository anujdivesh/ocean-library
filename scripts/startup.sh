#!/bin/sh
set -e

# Wait for database if enabled
if [ "$WAIT_FOR_DB" = "true" ]; then
  echo "Waiting for database to be ready..."
  /app/scripts/wait-for-db.sh
fi

# Initialize database if enabled
if [ "$INIT_DB" = "true" ]; then
  echo "Initializing database..."
  /app/scripts/init_db.sh
fi

# Start the application
exec "$@"