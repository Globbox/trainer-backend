from django.contrib import admin
from django.urls import path
from django.urls import include

from trainer_backend.common.api.routers import ExtendableRouter
from trainer_backend.user.routers import auth_router
from trainer_backend.user.routers import user_router

api_router = ExtendableRouter()
api_router.extend(auth_router)
api_router.extend(user_router)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
]
