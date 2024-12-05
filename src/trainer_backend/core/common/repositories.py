from abc import ABC
from abc import abstractmethod


class AbstractReadRepository(ABC):
    """Абстрактный класс репозитория для чтения."""

    @abstractmethod
    def _read(self, *args, **kwargs):
        """Чтение данных из репозитория."""


class AbstractCreateRepository(ABC):
    """Абстрактный класс репозитория для записи."""

    @abstractmethod
    def _write(self, *args, **kwargs):
        """Запись данных в репозиторий."""
