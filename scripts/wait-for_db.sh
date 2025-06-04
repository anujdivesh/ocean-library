#!/bin/bash
# scripts/wait-for-db.sh

host=db
port=5432
timeout=30

echo "Waiting for database to be ready..."
while ! nc -z $host $port; do
  sleep 1
  timeout=$((timeout - 1))
  if [ $timeout -eq 0 ]; then
    echo "Timeout waiting for database"
    exit 1
  fi
done
echo "Database is ready!"