#!/bin/sh

# '/bin/sh' is used by the postgres:xxx-alpine DB Docker image

export PGUSER="postgres"

psql -c "CREATE DATABASE inventory;"
psql inventory -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

# remember to "chmod +x db-setup.sh"