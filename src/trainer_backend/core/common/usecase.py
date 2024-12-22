from abc import ABC
from abc import abstractmethod
from typing import Sequence
from typing import Type


class AbstractUseCase(ABC):
    """Абстрактный класс UseCase."""

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Основной метод UseCase-а."""


class AbstractChainUseCase(AbstractUseCase):
    """Абстрактный класс цепочки UseCase-ов."""

    _use_cases: Sequence[Type[AbstractUseCase]]

    def __init__(self, *args, **kwargs):
        assert len(self._use_cases) == 0, ValueError('use_cases is empty')
        self.init_args = args
        self.init_kwargs = kwargs

    def execute(self, *args, **kwargs):
        """Основной метод UseCase-а."""
        use_case_iter = iter(self._use_cases)

        use_case_cls = next(use_case_iter)(
            *self.init_args, **self.init_kwargs
        )
        last_result = use_case_cls.execute(*args, **kwargs)

        for use_case_cls in use_case_iter:
            use_case_instance = use_case_cls(
                *self.init_args, **self.init_kwargs
            )
            last_result = use_case_instance.execute(
                *args, last_result=last_result, **kwargs
            )
