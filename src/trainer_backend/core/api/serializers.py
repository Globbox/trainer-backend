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
