"""Конфигурация для celery."""
from __future__ import absolute_import
from __future__ import unicode_literals

import os

from celery import Celery
from django.conf import settings
from kombu import Exchange
from kombu import Queue


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'phs.settings.prod'
)

celery_app = Celery('trainer')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

default_exchange = Exchange('trainer_default', type='direct')

celery_app.conf.update(
    task_queues=(
        Queue(
            name='default',
            exchange=default_exchange,
            routing_key='trainer_default'
        ),
    ),
    task_routes={
        '*.tasks.*': {'queue': 'default', 'routing_key': 'trainer_default'},
    },
    task_default_queue='default',
    task_default_exchange='default',
)

celery_app.autodiscover_tasks(settings.INSTALLED_APPS)


@celery_app.task(bind=True)
def debug_task(self, dt=None):
    """Тестовая таска."""
    return '{1} Request: {0!r}'.format(self.request, dt)


@celery_app.task(bind=True)
def debug_error_task(self):
    """Тестовая таска с ошибкой."""
    raise ValueError('Testing exception')
