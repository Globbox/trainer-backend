from rest_framework.routers import SimpleRouter

from .viewsets import AnswerViewSet
from .viewsets import EgeExamViewSet
from .viewsets import EgeTaskViewSet
from .viewsets import OgeExamViewSet
from .viewsets import OgeTaskViewSet
from .viewsets import ThematicSpeechContentViewSet


thematic_content_router = SimpleRouter()
thematic_content_router.register(
    'thematic-contents', ThematicSpeechContentViewSet,
    basename='thematic-content'
)


ege_router = SimpleRouter()
ege_router.register(
    'ege/exams', EgeExamViewSet,
    basename='ege-exams'
)
ege_router.register(
    'ege/tasks', EgeTaskViewSet,
    basename='ege-tasks'
)

oge_router = SimpleRouter()
oge_router.register(
    'oge/exams', OgeExamViewSet,
    basename='ege-exams'
)
oge_router.register(
    'oge/tasks', OgeTaskViewSet,
    basename='oge-tasks'
)


answer_router = SimpleRouter()
answer_router.register(
    'answers', AnswerViewSet, basename='answers'
)
