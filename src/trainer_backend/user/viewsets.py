from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from trainer_backend.core.api.responses import TextResponse
from trainer_backend.user.generators import account_activation_token

from .models import User
from .serializers import UserSerializer
from .serializers import UserWithPasswordSerializer
from .usecases import ResetUserPasswordUseCase


class AuthViewSet(viewsets.ViewSet):
    """API ViewSet для работы с аутентификацией."""

    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Метод API для регистрации."""
        serializer = UserWithPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()

        token = Token.objects.create(user=user)

        return TextResponse(
            token.key, status_code=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Метод API для входа в систему."""
        user = authenticate(
            email=request.data['email'],
            password=request.data['password']
        )

        if not user:
            return Response(
                {'error': 'Неверный логин или пароль'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)
        return TextResponse(
            token.key, status_code=status.HTTP_201_CREATED
        )

    @action(
        detail=False, methods=['post'], permission_classes=[IsAuthenticated],
    )
    def logout(self, request):
        """Метод API для выхода из текущей сессии."""
        Token.objects.get(
            user=request.user
        ).delete()
        return Response(
            {'message': 'Выполнен выход'},
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """API ViewSet для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_value_regex = r'\d+'

    @action(
        detail=False,
        methods=['get', 'put']
    )
    def me(self, request):
        """Метод API для получения/обновления данных о пользователе."""
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = self.get_serializer(
                user,
                data=request.data,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'error': "Неверный запрос"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=['post'],
        url_path='password-reset'
    )
    def password_reset(self, request):
        """Метод сброса пароля."""
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': "Пользователь с указанным email не найден."},
                status=status.HTTP_400_BAD_REQUEST
            )

        ResetUserPasswordUseCase().execute(user)
        return Response(
            {'message': (
                "Письмо для сброса пароля отправлено на почтовый ящик"
            )},
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['post'],
        url_path='password-reset-confirm/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)'
    )
    def password_reset_confirm(self, request, uidb64, token):
        """Метод подтверждения нового пароля."""
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and (
            account_activation_token.check_token(user, token)
        ):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response(
                {'message': "Пароль успешно изменен."},
                status=status.HTTP_200_OK
            )

        return Response(
            {'error': 'Токен недействителен или истек.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def get_permissions(self):
        """Получить доступы для ViewSet."""
        if self.action in [
            'password_reset_confirm',
            'password_reset',
        ]:
            return [AllowAny()]
        elif self.action in ['me']:
            return [IsAuthenticated()]

        return super().get_permissions()
