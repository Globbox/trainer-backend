from django.db.models import OuterRef
from django.db.models import Subquery
from rest_framework import serializers

from trainer_backend.core.api.serializers import Base64FileField
from trainer_backend.core.api.serializers import EnumField
from trainer_backend.trainer.enums import AnswerStatus
from trainer_backend.trainer.enums import ExamType
from trainer_backend.trainer.enums import TaskType
from trainer_backend.trainer.models import Answer
from trainer_backend.trainer.models import Exam
from trainer_backend.trainer.models import Image
from trainer_backend.trainer.models import Question
from trainer_backend.trainer.models import QuestionAnswer
from trainer_backend.trainer.models import QuestionAudioGuidance
from trainer_backend.trainer.models import Task
from trainer_backend.trainer.models import TaskAnswer
from trainer_backend.trainer.models import TaskTypeParameter
from trainer_backend.trainer.models import ThematicSpeechContent

from .mappers import AUDIO_GUIDANCE_FIELD_MAPPER


class QuestionAudioGuidanceSerializer(
    serializers.Serializer
):
    """Модель для хранения аудио сопровождения вопросов."""

    audio_guidance = serializers.FileField(
        allow_null=True,
        source='audio',
        label='Аудио файл',
    )

    class Meta:
        model = QuestionAudioGuidance
        fields = [
            'audio_guidance'
        ]


class TaskParameterSerializer(
    serializers.Serializer
):
    """Сериализатор параметров заданий."""

    number = serializers.IntegerField(
        label="Порядок задания в экзамене"
    )
    audio_guidance = serializers.FileField(
        source='audio',
        label='Аудио сопровождение',
    )
    preparation_seconds = serializers.IntegerField(
        label='Кол-во секунд на подготовку задания',
    )
    execution_seconds = serializers.IntegerField(
        required=False,
        label='Кол-во секунд на выполнение задания',
    )
    question_execution_seconds = serializers.IntegerField(
        required=False,
        label='Кол-во секунд на ответ',
    )

    class Meta:
        model = TaskTypeParameter
        fields = [
            'number', 'audio_guidance', 'preparation_seconds',
            'execution_seconds', 'question_execution_seconds'
        ]


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображений."""

    class Meta:
        model = Image
        fields = ['header', 'image']


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор вопросов."""

    _guidance_map = None

    def to_representation(self, instance: Question):
        """Преобразование в объект."""
        if self._guidance_map is None:
            self._guidance_map = {
                guidance.question_number: guidance
                for guidance in QuestionAudioGuidance.objects.all()
            }
        representation = super().to_representation(instance)
        question_guidance = self._guidance_map.get(
            instance.parent_tasks.first().number, {}
        )
        representation.update(
            QuestionAudioGuidanceSerializer(
                question_guidance, context=self.context
            ).data
        )
        return representation

    class Meta:
        model = Question
        fields = ['id', 'description', 'audio']


class ThematicSpeechContentSerializer(serializers.ModelSerializer):
    """Сериализатор тематического содержания речи."""

    class Meta:
        model = ThematicSpeechContent
        fields = ['id', 'short_designation', 'description']


class AudioGuidanceSerializer(serializers.Serializer):
    """Сериализатор аудио сопровождения."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in AUDIO_GUIDANCE_FIELD_MAPPER.items():
            self.fields[field] = serializers.FileField(required=False)


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор заданий."""

    _task_params_map = None

    type = EnumField( # noqa A003
        enum_class=TaskType, source='task_type'
    )
    exam = serializers.SerializerMethodField(
        read_only=True
    )
    thematic_speech_content = ThematicSpeechContentSerializer()
    images = serializers.SerializerMethodField(
        read_only=True
    )
    questions = serializers.SerializerMethodField(
        read_only=True
    )

    def get_images(self, instance):
        """Получить изображения для задания."""
        queryset = Image.objects.filter(
            parent_tasks__task=instance
        ).order_by('parent_tasks__number')

        return ImageSerializer(
            queryset, context=self.context, many=True
        ).data

    def get_questions(self, instance):
        """Получить вопросы для задания."""
        queryset = Question.objects.filter(
            parent_tasks__task=instance
        ).order_by('parent_tasks__number')

        return QuestionSerializer(
            queryset, context=self.context, many=True
        ).data

    def get_exam(self, instance):
        """Получить экзамен для задания."""
        task_exam = Exam.objects.filter(
            tasks__task=instance
        ).first()

        return ExamSerializer(
            task_exam, context={
                **self.context, 'with_tasks': False
            }, many=False
        ).data

    def to_representation(self, instance):
        """Преобразование в объект."""
        if self._task_params_map is None:
            self._task_params_map = {
                task.task_type: task
                for task in TaskTypeParameter.objects.all()
            }
        representation = super().to_representation(instance)
        task_params = self._task_params_map.get(representation['type'])
        if task_params is not None:
            representation.update(
                TaskParameterSerializer(
                    task_params, context=self.context
                ).data
            )
        return representation

    class Meta:
        model = Task
        fields = [
            'id',
            'type',
            'exam',
            'header',
            'description',
            'thematic_speech_content',
            'images',
            'audio',
            'questions',
        ]


class ExamSerializer(serializers.ModelSerializer):
    """Сериализатор модели экзамены."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.context.get('with_tasks', False):
            self.fields.pop('tasks')

    type = EnumField( # noqa A003
        enum_class=ExamType, source='exam_type'
    )
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, instance):
        """Получить задания для экзамена."""
        tasks = Task.objects.filter(
            exams__exam=instance
        ).annotate(
            task_number=Subquery(
                TaskTypeParameter.objects.filter(
                    task_type=OuterRef('task_type')
                ).values('number')[:1]
            )
        ).order_by('task_number')

        return TaskSerializer(
            tasks, context=self.context, many=True
        ).data

    class Meta:
        model = Exam
        fields = [
            'id',
            'number',
            'type',
            'tasks'
        ]


class QuestionAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели QuestionAnswer."""

    audio = Base64FileField()
    question = serializers.SerializerMethodField(read_only=True)
    question_id = serializers.IntegerField(write_only=True)

    def get_question(self, instance):
        """Получить вопросы."""
        return QuestionSerializer(instance.question).data

    class Meta:
        model = QuestionAnswer
        fields = ['id', 'question', 'question_id', 'audio']


class TaskAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели TaskAnswer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    questions = QuestionAnswerSerializer(many=True)
    audio = Base64FileField(allow_null=True, required=False)
    task = TaskSerializer(read_only=True)
    task_id = serializers.IntegerField(write_only=True)

    def get_questions(self, instance):
        """Получить вопросы."""
        questions = instance.questions.order_by('question_number')
        return QuestionAnswerSerializer(questions, many=True).data

    def get_task(self, instance):
        """Получить вопросы."""
        return TaskSerializer(instance.task, context=self.context).data

    class Meta:
        model = TaskAnswer
        fields = ['id', 'task', 'task_id', 'audio', 'questions']


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Answer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.context.get('with_tasks', False):
            self.fields.pop('tasks')

    tasks = TaskAnswerSerializer(many=True)
    status = EnumField(
        enum_class=AnswerStatus,
        read_only=True,
    )

    def get_tasks(self, obj):
        """Получить задания."""
        tasks = obj.tasks.order_by('task_number')
        return TaskAnswerSerializer(
            tasks, context=self.context, many=True
        ).data

    class Meta:
        model = Answer
        fields = [
            'id', 'created_at', 'status', 'full_audio', 'answer_archive',
            'tasks'
        ]
