#!/bin/bash

# Initialize database if needed
if [ "$INIT_DB" = "true" ]; then
    echo "Initializing database from backup..."
    psql -h db -U postgres -d library_db -f /app/library.sql
fi

# Run the application
exec "$@"