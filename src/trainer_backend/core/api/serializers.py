import base64
import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import serializers


class EnumField(serializers.Field):
    """Сериализатор для полей перечислений."""

    def __init__(self, enum_class, **kwargs):
        self.enum_class = enum_class
        super().__init__(**kwargs)

    def to_representation(self, value):
        """Преобразование в объект."""
        if isinstance(value, self.enum_class):
            return value.value
        return value

    def to_internal_value(self, data):
        """Преобразование из объекта."""
        try:
            return self.enum_class[data]
        except ValueError:
            raise serializers.ValidationError(
                f"Invalid value: {data}. "
                f"Allowed values are: {[e.value for e in self.enum_class]}")


class Base64FileField(serializers.FileField):
    """Поле для работы с Base64 данными."""

    trust_provided_content_type = True

    def to_representation(self, value):
        """Преобразование в объект."""
        if not value:
            return None

        try:
            with value.open('rb') as audio_file:
                return base64.b64encode(audio_file.read()).decode('utf-8')
        except Exception:
            raise serializers.ValidationError("Ошибка преобразование base64")

    def to_internal_value(self, base64_data):
        """Преобразование из объекта."""
        if not isinstance(base64_data, str):
            raise serializers.ValidationError("Неверный тип данных")

        file_mime_type = None
        if ";base64," in base64_data:
            header, base64_data = base64_data.split(";base64,")
            if self.trust_provided_content_type:
                file_mime_type = header.replace('data:', '')

        try:
            decoded_file = base64.b64decode(base64_data)
        except TypeError:
            raise serializers.ValidationError("Invalid base64 data")

        upload_file = SimpleUploadedFile(
            name=str(uuid.uuid4()),
            content=decoded_file,
            content_type=file_mime_type
        )
        return super().to_internal_value(upload_file)
