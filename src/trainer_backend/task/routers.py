from rest_framework.routers import SimpleRouter

from trainer_backend.task.viewsets import TaskViewSet


router = SimpleRouter()
router.register('tasks', TaskViewSet, basename='tasks')
