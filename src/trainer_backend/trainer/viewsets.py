from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from trainer_backend.core.api.viewsets import QueryParamMixin

from .enums import ExamType
from .mappers import AUDIO_GUIDANCE_FIELD_MAPPER
from .models import Answer
from .models import AudioGuidance
from .models import Exam
from .models import Task
from .models import ThematicSpeechContent
from .repositories import AnswerRepository
from .serializers import AnswerSerializer
from .serializers import AudioGuidanceSerializer
from .serializers import ExamSerializer
from .serializers import TaskAnswerSerializer
from .serializers import TaskSerializer
from .serializers import ThematicSpeechContentSerializer
from .tasks import process_answer_task


class BaseSimpleModelViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    """Базовый простой ViewSet для моделей."""

    permission_classes = (AllowAny,)
    ordering = ('pk',)
    lookup_value_regex = r'\d+'
    pagination_class = None


class ThematicSpeechContentViewSet(BaseSimpleModelViewSet):
    """API тематического содержания речи."""

    queryset = ThematicSpeechContent.objects.all()
    serializer_class = ThematicSpeechContentSerializer


class AudioGuidanceViewSet(GenericViewSet):
    """API аудио сопровождения."""

    permission_classes = (AllowAny,)
    queryset = AudioGuidance.objects.all()
    serializer_class = AudioGuidanceSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):  # noqa A003
        """Получить данные по аудио сопровождению."""
        audio_guidance = {
            AUDIO_GUIDANCE_FIELD_MAPPER[
                audio_guidance.guidance_type
            ]: audio_guidance.audio
            for audio_guidance in self.filter_queryset(self.get_queryset())
        }

        return Response(self.get_serializer(audio_guidance).data)


class TaskViewSet(
    QueryParamMixin, BaseSimpleModelViewSet
):
    """ViewSet для работы с вопросами."""

    _exam_type: ExamType = None
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert self._exam_type, ValueError('Необходимо указать тип экзамена')

    def get_queryset(self):
        """Получить QuerySet."""
        queryset = super().get_queryset().filter(
            exams__exam__exam_type=self._exam_type,
        )

        fipi = self._get_query_bool('fipi')

        if fipi is not None:
            queryset = queryset.filter(
                exams__exam__fipi=fipi
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
                task_type=task_type
            )

        exam_id = self._get_query_param(
            'exam_id', converter=int
        )

        if exam_id is not None:
            queryset = queryset.filter(
                exams__exam__id__in=[exam_id]
            )

        return queryset


class ExamViewSet(QueryParamMixin, BaseSimpleModelViewSet):
    """ViewSet для работы с экзаменами."""

    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_serializer_context(self):
        """Получить контекст сериализатора."""
        context = super().get_serializer_context()
        return {**context, 'with_tasks': self._get_query_bool('with_tasks')}

    def get_queryset(self):
        """Получить QuerySet."""
        queryset = super().get_queryset()
        fipi = self._get_query_bool('fipi')

        if fipi is not None:
            queryset = queryset.filter(
                fipi=fipi
            )

        return queryset


class EgeExamViewSet(ExamViewSet):
    """ViewSet для работы с экзаменами ЕГЭ."""

    def get_queryset(self):
        """Получить QuerySet."""
        return super().get_queryset().filter(
            exam_type=ExamType.EGE
        )


class OgeExamViewSet(ExamViewSet):
    """ViewSet для работы с экзаменами ЕГЭ."""

    def get_queryset(self):
        """Получить QuerySet."""
        return super().get_queryset().filter(
            exam_type=ExamType.OGE
        )


class EgeTaskViewSet(TaskViewSet):
    """ViewSet для работы с заданиями ЕГЭ."""

    _exam_type: ExamType = ExamType.EGE


class OgeTaskViewSet(TaskViewSet):
    """ViewSet для работы с заданиями ЕГЭ."""

    _exam_type: ExamType = ExamType.OGE


class AnswerViewSet(
    QueryParamMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.ListModelMixin, GenericViewSet
):
    """ViewSet для работы с ответами."""

    queryset = Answer.objects.all()

    ordering = ('pk',)
    lookup_value_regex = r'\d+'
    serializer_class = AnswerSerializer
    pagination_class = None
    permission_classes = (AllowAny,)
    answer_repository_class = AnswerRepository

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.answer_repository = self.answer_repository_class()

    def get_serializer_context(self):
        """Получить контекст сериализатора."""
        context = super().get_serializer_context()
        return {
            **context,
            'with_tasks': self._get_query_bool(
                'with_tasks', default=False
            ),
        }

    def list(self, request, *args, **kwargs): # noqa A003
        """Получить ответы."""
        queryset = self.filter_queryset(self.get_queryset().filter(
            user=request.user
        ))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, pk=None, **kwargs):
        """Получить ответ."""
        try:
            answer = self.get_queryset().get(pk=pk)
        except Answer.DoesNotExist:
            return Response(
                {"detail": "Ответ не найден."},
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            self.get_serializer(answer).data, status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        """Создать объект."""
        serializer = TaskAnswerSerializer(
            data=request.data, many=True, context={'with_tasks': True}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        # Создание ответа
        answer = self.answer_repository.create_answer(
            user=request.user if request.user.is_authenticated else None
        )
        self.answer_repository.add_tasks_answer(
            answer, serializer.validated_data
        )

        process_answer_task.delay(answer_id=answer.id)
        return Response(
            self.get_serializer(answer).data
        )
