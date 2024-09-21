from abc import ABC
from abc import abstractmethod


class AbstractReadDataProvider(ABC):
    """Абстрактный класс провайдера данных для чтения."""

    @abstractmethod
    def get(self, *args, **kwargs):
        """Чтение данных из репозитория."""


class AbstractCreateDataProvider(ABC):
    """Абстрактный класс провайдера данных для записи."""

    @abstractmethod
    def set(self, *args, **kwargs):
        """Запись данных в репозиторий."""
