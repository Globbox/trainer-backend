#!/bin/bash

python ${PROJECT_ROOT}/manage.py collectstatic --noinput
#python ${PROJECT_ROOT}/manage.py migrate TODO: move to migration script

gunicorn --config gunicorn.conf.py trainer_backend.wsgi:application
