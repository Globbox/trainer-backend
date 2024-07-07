from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    """Конфигурация приложения Аутентификация."""

    name = __package__
