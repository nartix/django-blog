#!/bin/bash

# Run the update certificate script
./update_cert.sh $1

# If the update script succeeds, start the Django server
if [ $? -eq 0 ]; then
    if [ "$1" == "prod" ]; then
        # Production server
        gunicorn ferozfaiz.wsgi:application --bind 0.0.0.0:8000
    elif [ "$1" == "celery" ]; then
        celery --workdir ferozfaiz -A ferozfaiz worker -l INFO
    elif [ "$1" == "kafka" ]; then
        python ferozfaiz/manage.py startkafkaconsumer $KAFKA_TOPIC $KAFKA_TOPIC_GROUP --commit
    else
        # Development server
        python app/ferozfaiz/manage.py runserver 0.0.0.0:8000
    fi
else
    echo "PostgreSQL certificate update failed."
    exit 1
fi