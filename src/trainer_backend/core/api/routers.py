from rest_framework.routers import DefaultRouter


class ExtendableRouter(DefaultRouter):
    """Расширяет функциональность `DefaultRouter`.

    Добавлен метод для реализации вложенного роутинга.
    """

    include_format_suffixes = False

    def extend(self, router):
        """Расширяет роутинг."""
        self.registry = list(set(self.registry) | set(router.registry))
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        self._urls = list(set(self._urls) | set(router.urls))
