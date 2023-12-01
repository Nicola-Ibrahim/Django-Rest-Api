#!/usr/bin/env bash

set -e
source .venv/bin/activate

RUN_MANAGE_PY='python manage.py'

echo "----- Generate JWT siging key ------"
# Create the .keys folder
mkdir ./config/settings/.keys

# Check if the file exists
if [ -f ./config/settings/.keys/jwtHS256.key ]; then
  echo "The key file already exists. No new key is generated."
  exit 1
else
  openssl rand -base64 32 > ./config/settings/.keys/jwtHS256.key
fi

echo "----- Collect static files ------"
$RUN_MANAGE_PY collectstatic --noinput

echo "-----------Apply migration---------"
$RUN_MANAGE_PY migrate --noinput

$RUN_MANAGE_PY makesuperuser

echo "-----Starting the DREST API------"
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application
