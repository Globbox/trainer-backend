from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        """Создать объект."""
        if not validated_data.get('password'):
            raise serializers.ValidationError("Password - обязательное поле")

        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'first_name', 'second_name', 'birthdate',
            'phone'
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()