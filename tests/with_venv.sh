#!/bin/bash

export DJANGO_LIVE_TEST_SERVER_ADDRESS="localhost:8000-8010,8080,9200-9300"
export DJANGO_TEST_PROCESSES="1"
TESTS=`dirname $0`
VENV=$TESTS/../$1
shift

if [ ! -f "$VENV/bin/activate" ]; then
    echo "Virtual environment not found at $VENV"
    echo "Please run 'make develop' first"
    exit 1
fi

source "$VENV/bin/activate"
exec "$@"