from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'second_name', 'birthdate', 'phone'
        ]


class UserWithPasswordSerializer(UserSerializer):
    """Сериализатор пользователей с паролем."""

    password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        """Создать объект."""
        if not validated_data.get('password'):
            raise serializers.ValidationError("Password - обязательное поле")

        return User.objects.create_user(**validated_data)

    class Meta(UserSerializer.Meta):
        fields = [*UserSerializer.Meta.fields, 'password']
