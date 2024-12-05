from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class ApiBadRequestException(APIException):
    """Ошибка 400 при работе с API."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Ошибка при работе с API')
    default_code = 'error'

    def __init__(self, detail=None) -> None:
        super().__init__(detail=detail)


class ApiNotFoundException(APIException):
    """Ошибка 404 при работе с API."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Данные не найдены')
    default_code = 'not_found'

    def __init__(self, detail=None) -> None:
        super().__init__(detail=detail)


class ApiUniqueConstraintException(APIException):
    """Ошибка 404 при нарушении уникальности."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Запись уже существует')
    default_code = 'already_exists'
