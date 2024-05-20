#!/bin/sh

# Add Static Files
python ${APP_ROOT}/manage.py collectstatic --noinput

# Migrate
python ${APP_ROOT}/manage.py migrate

# Run Gunicorn WSGI
gunicorn --config gunicorn.conf.py trainer_backend.wsgi:application

exec "$@"