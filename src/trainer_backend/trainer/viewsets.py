from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from trainer_backend.core.api.viewsets import QueryParamMixin

from .data_providers import AnswerTaskCreateDataProvider
from .enums import ExamType
from .models import Answer
from .models import Exam
from .models import Task
from .models import ThematicSpeechContent
from .serializers import AnswerSerializer
from .serializers import ExamSerializer
from .serializers import ExtendedExamSerializer
from .serializers import ExtendedTaskSerializer
from .serializers import TaskAnswerSerializer
from .serializers import TaskSerializer
from .serializers import ThematicSpeechContentSerializer
from .tasks import generate_answer_archive


class ThematicSpeechContentViewSet(ReadOnlyModelViewSet):
    """API тематического содержания речи."""

    queryset = ThematicSpeechContent.objects.all()
    serializer_class = ThematicSpeechContentSerializer
    ordering = ('pk',)
    lookup_value_regex = r'\d+'
    pagination_class = None
    permission_classes = (AllowAny,)


class ExamViewSet(QueryParamMixin, ReadOnlyModelViewSet):
    """ViewSet для работы с экзаменами."""

    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    ordering = ('pk',)
    lookup_value_regex = r'\d+'
    pagination_class = None
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """Получить QuerySet."""
        queryset = super().get_queryset()

        fipi = self._get_query_bool('fipi')

        if fipi is not None:
            queryset = queryset.filter(
                fipi=fipi
            )

        return queryset

    def get_serializer_class(self):
        """Получить сериализатор."""
        if self.action == 'retrieve':
            return ExtendedExamSerializer
        return super().get_serializer_class()


class TaskViewSet(QueryParamMixin, ReadOnlyModelViewSet):
    """ViewSet для работы с вопросами."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    ordering = ('pk',)
    lookup_value_regex = r'\d+'
    pagination_class = None
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """Получить QuerySet."""
        queryset = super().get_queryset()

        fipi = self._get_query_bool('fipi')

        if fipi is not None:
            queryset = queryset.filter(
                exams_fipi=fipi
            )

        thematic_content_id = self._get_query_param(
            'thematic_content_id', converter=int
        )

        if thematic_content_id is not None:
            queryset = queryset.filter(
                thematic_speech_content=thematic_content_id
            )

        task_type = self._get_query_param(
            'task_type', converter=int
        )

        if task_type is not None:
            queryset = queryset.filter(
                type=task_type
            )

        return queryset

    def get_serializer_class(self):
        """Получить сериализатор."""
        if self.action == 'retrieve':
            return ExtendedTaskSerializer
        return super().get_serializer_class()


class EgeExamViewSet(ExamViewSet):
    """ViewSet для работы с экзаменами ЕГЭ."""

    def get_queryset(self):
        """Получить QuerySet."""
        return super().get_queryset().filter(
            type=ExamType.EGE
        )


class OgeExamViewSet(ExamViewSet):
    """ViewSet для работы с экзаменами ЕГЭ."""

    def get_queryset(self):
        """Получить QuerySet."""
        return super().get_queryset().filter(
            type=ExamType.OGE
        )


class EgeTaskViewSet(TaskViewSet):
    """ViewSet для работы с заданиями ЕГЭ."""

    def get_queryset(self):
        """Получить QuerySet."""
        return super().get_queryset().filter(
            exams__exam__type=ExamType.EGE
        )


class OgeTaskViewSet(TaskViewSet):
    """ViewSet для работы с заданиями ЕГЭ."""

    def get_queryset(self):
        """Получить QuerySet."""
        return super().get_queryset().filter(
            exams__exam__type=ExamType.OGE
        )


class AnswerViewSet(QueryParamMixin, ModelViewSet):
    """ViewSet для работы с ответами."""

    queryset = Answer.objects.all()

    ordering = ('pk',)
    lookup_value_regex = r'\d+'
    serializer_class = AnswerSerializer
    pagination_class = None
    permission_classes = (AllowAny,)
    create_data_provider_class = AnswerTaskCreateDataProvider

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_data_provider = self.create_data_provider_class()

    def create(self, request, *args, **kwargs):
        """Создать объект."""
        serialize_answer = TaskAnswerSerializer(data=request.data, many=True)
        if not serialize_answer.is_valid():
            return Response(
                serialize_answer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        answer = self.create_data_provider.set(serialize_answer.validated_data)

        generate_answer_archive.delay(answer_id=answer.id)
        return Response(AnswerSerializer(answer).data)
