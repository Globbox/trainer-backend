from django.contrib import admin
from django.urls import include
from django.urls import path

from trainer_backend.core.api.routers import ExtendableRouter
from trainer_backend.trainer.routers import answer_router
from trainer_backend.trainer.routers import audio_guidance_router
from trainer_backend.trainer.routers import ege_router
from trainer_backend.trainer.routers import oge_router
from trainer_backend.trainer.routers import thematic_content_router
from trainer_backend.user.routers import auth_router
from trainer_backend.user.routers import user_router


api_router = ExtendableRouter()
api_router.extend(auth_router)
api_router.extend(user_router)
api_router.extend(audio_guidance_router)
api_router.extend(thematic_content_router)
api_router.extend(ege_router)
api_router.extend(oge_router)
api_router.extend(answer_router)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
]
