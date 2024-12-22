import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Команда для ожидания подключения к БД."""

    help = 'Команда для ожидания подключения к БД' # noqa A003

    _wait_timeout = 120

    def handle(self, *args, **options):
        """Выполнение команды."""
        self.stdout.write('Waiting database connection...')
        connected, start = False, time.time()
        while not connected and time.time() - start < self._wait_timeout:
            try:
                connections['default'].cursor().execute("SELECT 1")
                connected = True
            except OperationalError:
                time.sleep(1)
