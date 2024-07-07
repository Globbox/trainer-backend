from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer


class AuthViewSet(viewsets.ViewSet):
    """"""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Метод API для регистрации."""
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({'id': user.id, 'token': token.key},
                        status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Метод API для регистрации."""
        user = authenticate(
            email=request.data['email'],
            password=request.data['password']
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'id': user.id,
                'token': token.key
            })
        else:
            return Response({'error': 'Неверный логин или пароль'},
                            status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'],
            permission_classes=[IsAuthenticated])
    def logout(self, request):
        Token.objects.get(user=request.user).delete()
        return Response({'message': 'Выполнен выход'},
                        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
