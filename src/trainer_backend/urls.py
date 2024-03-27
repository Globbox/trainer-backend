from django.contrib import admin
from django.urls import path
from django.urls import include

from trainer_backend.common.api.routers import ExtendableRouter

api_router = ExtendableRouter()


urlpatterns = [
    path('', admin.site.urls),
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
]
