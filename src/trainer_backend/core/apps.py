from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    """Конфигурация основного приложения."""

    name = __package__

    verbose_name = 'Основная конфигурация'
