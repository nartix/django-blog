#!/bin/bash

# This script is used to update the root certificate for the PostgreSQL database.
# In production Docker Compose, Vault Agent renders the cert file directly.
# For older/dev flows, POSTGRESQL_CRT can still be used to write the cert file.

if [ "$1" == "prod" ] || [ "$1" == "celery" ] || [ "$1" == "kafka" ]; then
    CERT_FILE="$PG_SSL_ROOT_CERT"
else
    CERT_FILE="$POSTGRESQL_SSL_ROOT_CERT_DJANGO_DEV"
fi

if [ -z "$CERT_FILE" ]; then
    echo "Error: PostgreSQL certificate path is not set."
    exit 1
fi

if [ -s "$CERT_FILE" ]; then
    echo "Using existing PostgreSQL certificate at $CERT_FILE."
    exit 0
fi

# Create the directory if it doesn't exist
mkdir -p "$(dirname "$CERT_FILE")"

# Check if the POSTGRESQL_CRT environment variable is set and not empty
if [ -z "$POSTGRESQL_CRT" ]; then
    echo "Error: PostgreSQL certificate was not rendered and POSTGRESQL_CRT is not set."
    exit 1
else
    echo "$POSTGRESQL_CRT" > "$CERT_FILE"
    echo "Updated $CERT_FILE with POSTGRESQL_CRT data."
fi
exit 0
