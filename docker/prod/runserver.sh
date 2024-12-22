#!/bin/sh

# Add Static Files
python ${PROJECT_ROOT}/manage.py collectstatic --noinput

# Wait Database connection
python ${PROJECT_ROOT}/manage.py wait_for_db

# Migrate
python ${PROJECT_ROOT}/manage.py migrate

# Create Admin User
python ${PROJECT_ROOT}/manage.py init_admin

# Run Gunicorn WSGI
gunicorn --config gunicorn.conf.py trainer_backend.wsgi:application

exec "$@"