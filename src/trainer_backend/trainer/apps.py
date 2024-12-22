from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    """Конфигурация приложения Тренажер."""

    name = __package__

    verbose_name = 'Тренажер'
