#!/bin/bash

# This script is used to update the root certificate for the PostgreSQL database.
# Root certificate is retrieved from the POSTGRESQL_CRT environment variable.
# POSTGRESQL_CRT environment variable is set by envconsul when the container starts.

if [ "$1" == "prod" ] || [ "$1" == "celery" ] || [ "$1" == "kafka" ]; then
    CERT_FILE="$PG_SSL_ROOT_CERT"
else
    CERT_FILE="$POSTGRESQL_SSL_ROOT_CERT_DJANGO_DEV"
fi

# Create the directory if it doesn't exist
mkdir -p "$(dirname "$CERT_FILE")"

# Check if the POSTGRESQL_CRT environment variable is set and not empty
if [ -z "$POSTGRESQL_CRT" ]; then
    echo "Error: POSTGRESQL_CRT environment variable is not set."
    exit 1
else
    echo "$POSTGRESQL_CRT" > "$CERT_FILE"
    echo "Updated $CERT_FILE with POSTGRESQL_CRT data."
fi
exit 0