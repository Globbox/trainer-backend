from django.conf import settings
from django.core.management.base import BaseCommand

from trainer_backend.user.models import User


class Command(BaseCommand):
    """Команда для создания администратора."""

    help = 'Команда для создания администратора'

    _wait_timeout = 120

    def handle(self, *args, **options):
        """Выполнение команды."""
        self.stdout.write('Create admin user')

        if settings.DEFAULT_ADMIN_USERNAME.strip() == '':
            raise ValueError("Не задан пользователь")

        if settings.DEFAULT_ADMIN_PASSWORD.strip() == '':
            raise ValueError("Не задан пароль")

        if User.objects.filter(
            email=settings.DEFAULT_ADMIN_USERNAME
        ).exists():
            self.stdout.write('User already exists')
            return

        User.objects.create_superuser(
            settings.DEFAULT_ADMIN_USERNAME,
            password=settings.DEFAULT_ADMIN_PASSWORD
        )

        self.stdout.write('User successfully created')
