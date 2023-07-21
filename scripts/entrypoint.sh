#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python manage.py'

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

# exec poetry run gunicorn config.wsgi:application -p 8000 -b 0.0.0.0
exec poetry run gunicorn --bind 0.0.0.0:8000 config.wsgi
