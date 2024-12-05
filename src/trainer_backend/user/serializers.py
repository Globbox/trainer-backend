from rest_framework import serializers

from trainer_backend.core.api.exceptions import ApiUniqueConstraintException

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'second_name', 'birthdate', 'phone'
        ]


class LoginUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для входа."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'email', 'password'
        ]


class RegisterUserSerializer(LoginUserSerializer):
    """Сериализатор для регистрации пользователей."""

    def create(self, validated_data):
        """Создать объект."""
        if User.objects.filter(
            email=validated_data.get('email')
        ).exists():
            raise ApiUniqueConstraintException(
                detail='Пользователь с таким email уже существует'
            )
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'second_name', 'birthdate', 'phone',
            'password'
        ]
