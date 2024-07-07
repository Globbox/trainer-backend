#!/bin/bash

python ${PROJECT_ROOT}/manage.py collectstatic --noinput
# TODO: move to migration script
python ${PROJECT_ROOT}/manage.py migrate

gunicorn --config gunicorn.conf.py trainer_backend.wsgi:application
