#!/bin/bash

# Get the absolute path to the my-sql-agent directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Load environment variables from .env
set -a
source "$PROJECT_ROOT/.env"
set +a

# Function to check if postgres is ready
wait_for_postgres() {
    echo "Waiting for PostgreSQL to be ready..."
    until PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c '\q' 2>/dev/null; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done
    echo "PostgreSQL is up"
}

# Parse command line arguments
CLEAN=false
for arg in "$@"
do
    case $arg in
        --clean)
        CLEAN=true
        shift # Remove --clean from processing
        ;;
    esac
done

# Wait for PostgreSQL
wait_for_postgres

if [ "$CLEAN" = true ]; then
    echo "Dropping existing database..."
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>/dev/null
fi

echo "Creating database..."
PGPASSWORD=$DB_PASSWORD createdb -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME 2>/dev/null || true

echo "Initializing schema..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "$PROJECT_ROOT/sql/init.sql"

echo "Loading test data..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "$PROJECT_ROOT/sql/test_data.sql"

echo "Done! Database is ready." 