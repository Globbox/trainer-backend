from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class TextResponse(Response):
    """Класс ответа в виде текста."""

    def __init__(self, text, status_code=HTTP_200_OK):
        super(TextResponse, self).__init__(
            data=text, status=status_code, content_type='text/plain'
        )


class BaseApiResponse(Response):
    """Базовый класс API ответа."""

    _status = None

    def __init__(self, data):
        super(BaseApiResponse, self).__init__(
            data=data, status=self._status
        )


class BaseApiMessageResponse(BaseApiResponse):
    """Базовый класс API ответа с сообщением."""

    def __init__(self, message):
        super().__init__({'message': message})


class SuccessResponse(BaseApiMessageResponse):
    """Успешный API ответ."""

    _status = HTTP_200_OK
