class ApiException(Exception):
    """Ошибка при работе с API."""

    def __init__(self, status, body=None) -> None:
        """Добавляет HTTP-статус и тело ответа."""
        self.status = status
        self.body = body
        super().__init__(status, body)
