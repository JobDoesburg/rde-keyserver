#!/bin/bash

set -e

echo "Running application"

chown -R www-data:www-data /code/

cd /code/keyserver

python manage.py collectstatic --no-input
python manage.py migrate --no-input

uwsgi --ini /code/uwsgi.ini
