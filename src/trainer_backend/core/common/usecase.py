from abc import ABC
from abc import abstractmethod


class AbstractUseCase(ABC):
    """Абстрактный класс UseCase."""

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Основной метод UseCase-а."""
