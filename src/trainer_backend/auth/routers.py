from rest_framework.routers import SimpleRouter

from trainer_backend.auth.viewsets import UserViewSet


router = SimpleRouter()
router.register('auth', UserViewSet, basename='auth')
