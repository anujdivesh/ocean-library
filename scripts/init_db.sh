#!/bin/bash
set -e  # Exit immediately if any command fails

echo "Initializing database..."
start_time=$(date +%s)

# Create tables first
python -m app.init_db

# Then load data
python -m app.data_loader.load_countries
python -m app.data_loader.load_years
python -m app.data_loader.load_document_types
python -m app.data_loader.load_documents

end_time=$(date +%s)
echo "Database initialized in $((end_time - start_time)) seconds"