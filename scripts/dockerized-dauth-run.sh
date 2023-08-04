#!/usr/bin/env bash

set -e
source .venv/bin/activate

RUN_MANAGE_PY='python manage.py'

echo "----- Collect static files ------"
$RUN_MANAGE_PY collectstatic --noinput

echo "-----------Apply migration---------"
$RUN_MANAGE_PY migrate --noinput

$RUN_MANAGE_PY makesuperuser

echo "-----Starting the DAUTH API------"
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application
