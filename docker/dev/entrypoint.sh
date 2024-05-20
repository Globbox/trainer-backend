#!/bin/sh

# Add Static Files
python ${PROJECT_ROOT}/manage.py collectstatic --noinput

# Wait Database connection
python ${PROJECT_ROOT}/manage.py wait_for_db

# Migrate
python ${PROJECT_ROOT}/manage.py migrate

# Create Admin User
python ${PROJECT_ROOT}/manage.py init_admin

# Run Server
python ${PROJECT_ROOT}/manage.py runserver 0.0.0.0:8000

exec "$@"