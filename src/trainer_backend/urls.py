from django.contrib import admin
from django.urls import path
from django.urls import include

from trainer_backend.common.api.routers import ExtendableRouter
from trainer_backend.auth.routers import router as auth_router
from trainer_backend.task.routers import router as task_router

api_router = ExtendableRouter()
api_router.extend(auth_router)
api_router.extend(task_router)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
]
