from datetime import datetime

from attrs.converters import to_bool
from django.conf import settings
from rest_framework.exceptions import ParseError


class QueryParamMixin:
    """Миксин получения query-параметров."""

    def _get_query_param(
        self,
        param_name,
        required=False,
        allow_null=True,
        default=None,
        converter=None
    ):
        """Получить query-параметр по имени."""
        if required and param_name not in self.request.query_params:
            raise ParseError(detail=f'Параметр {param_name} обязателен')

        value = self.request.query_params.get(param_name, default)
        if not allow_null and value is None:
            raise ParseError(
                detail=f'Параметр {param_name} не может быть пустым'
            )

        if converter and value is not None:
            value = converter(value)

        return value

    def _get_query_date(
        self,
        param_name,
        required=False,
        allow_null=True,
        default=None
    ):
        """Получить дату из query по имени."""
        def _to_date(dt):
            try:
                return datetime.strptime(dt, settings.API_DATE_FORMAT)
            except ValueError:
                raise ParseError(
                    detail=(
                        f'Поле {param_name} должно иметь формат '
                        f'"{settings.API_DATE_FORMAT}"'
                    )
                )

        return self._get_query_param(
            param_name,
            required=required,
            allow_null=allow_null,
            default=default,
            converter=_to_date
        )

    def _get_query_bool(
        self,
        param_name,
        required=False,
        allow_null=True,
        default=None
    ):
        """Получить bool из query по имени."""
        def _to_bool(value):
            try:
                return to_bool(value)
            except ValueError:
                raise ParseError(
                    detail=(
                        f'Невозможно конвертировать поле "{param_name}" в bool'
                    )
                )

        return self._get_query_param(
            param_name,
            required=required,
            allow_null=allow_null,
            default=default,
            converter=_to_bool
        )
