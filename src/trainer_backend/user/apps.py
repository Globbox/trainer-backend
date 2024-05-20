from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    """Конфигурация приложения Пользователи."""

    name = __package__

    verbose_name = 'Пользователи'
