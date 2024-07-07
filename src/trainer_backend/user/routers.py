from rest_framework.routers import SimpleRouter

from trainer_backend.user.viewsets import AuthViewSet
from trainer_backend.user.viewsets import UserViewSet


auth_router = SimpleRouter()
auth_router.register('auth', AuthViewSet, basename='auth')

user_router = SimpleRouter()
user_router.register('users', UserViewSet, basename='users')
