from abc import ABC

from django.db.models import Q

from trainer_backend.core.common.repositories import AbstractCreateRepository
from trainer_backend.core.common.repositories import AbstractReadRepository


class BaseModelRepository(
    AbstractReadRepository, AbstractCreateRepository, ABC
):
    """Абстрактный класс репозитория для чтения."""

    _model = None

    def __init__(self):
        assert self._model, ValueError('Необходимо указать модель')

    def _get_filters(self, filters):
        """Возвращает фильтры для queryset-а."""
        arg_filters, kwarg_filters = [], {}

        if isinstance(filters, Q):
            arg_filters.append(filters)
        elif isinstance(filters, dict):
            kwarg_filters.update(filters)
        elif isinstance(filters, (list, tuple)):
            for f in filters:
                a_filters, k_filters = self._get_filters(f)
                arg_filters.extend(a_filters)
                kwarg_filters.update(k_filters)

        return arg_filters, kwarg_filters

    def _read(
            self, filters=None, excludes=None, annotations=None,
            pre_annotations=None, aggregates=None, extras=None, values=None,
            values_list=None, flat=False, distinct=False
    ):
        """Чтение данных из репозитория."""
        queryset = self._model.objects.all()

        if pre_annotations:
            queryset = queryset.annotate(**pre_annotations)

        if filters:
            arg_filters, kwarg_filters = self._get_filters(filters)
            queryset = queryset.filter(*arg_filters, **kwarg_filters)

        if extras:
            queryset = queryset.extra(**extras)

        if excludes:
            arg_filters, kwarg_filters = self._get_filters(excludes)
            queryset = queryset.exclude(*arg_filters, **kwarg_filters)

        if values:
            fields = values.get('fields', [])
            expressions = values.get('expressions', {})
            queryset = queryset.values(*fields, **expressions)

        if annotations:
            queryset = queryset.annotate(**annotations)

        if aggregates:
            queryset = queryset.aggregate(**aggregates)

        if values_list:
            queryset = queryset.values_list(*values_list, flat=flat)

        if distinct:
            queryset = queryset.distinct()

        return queryset

    def _write(self, *args, **kwargs):
        """Запись данных в репозиторий."""
        instance = self._model(**kwargs)
        instance.save()
        return instance
