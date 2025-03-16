#!/bin/sh

celery -A trainer_backend.celery_config:celery_app worker -l INFO -n trainer-worker@%n -Q default