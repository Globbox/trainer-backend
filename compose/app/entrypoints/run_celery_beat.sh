#!/bin/sh

celery --app=trainer_backend.celery_config:celery_app beat -l INFO --pidfile /tmp/celerybeat.pid -s /tmp/celerybeat-schedule