import os

from django.conf import settings
from django.db.models import OuterRef
from django.db.models import Subquery
from rest_framework import serializers

from trainer_backend.core.api.serializers import Base64FileField
from trainer_backend.core.api.serializers import EnumField
from trainer_backend.trainer.enums import AudioGuidanceType
from trainer_backend.trainer.enums import ExamType
from trainer_backend.trainer.enums import TaskType
from trainer_backend.trainer.mixins import AddAudioGuidanceMixin
from trainer_backend.trainer.mixins import AddQuestionAudioGuidanceMixin
from trainer_backend.trainer.mixins import AddTaskParametersMixin
from trainer_backend.trainer.models import Answer
from trainer_backend.trainer.models import Exam
from trainer_backend.trainer.models import Image
from trainer_backend.trainer.models import Question
from trainer_backend.trainer.models import Task
from trainer_backend.trainer.models import TaskTypeParameter
from trainer_backend.trainer.models import ThematicSpeechContent


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображений."""

    class Meta:
        model = Image
        fields = ['header', 'image']


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор вопросов."""

    class Meta:
        model = Question
        fields = ['description', 'audio']


class ThematicSpeechContentSerializer(serializers.ModelSerializer):
    """Сериализатор тематического содержания речи."""

    class Meta:
        model = ThematicSpeechContent
        fields = ['id', 'short_designation', 'description']


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор заданий."""

    type = EnumField(
        enum_class=TaskType
    )
    thematic_speech_content = ThematicSpeechContentSerializer()

    class Meta:
        model = Task
        fields = [
            'id',
            'type',
            'header',
            'description',
            'thematic_speech_content',
        ]


class ExtendedTaskSerializer(
    AddTaskParametersMixin, AddQuestionAudioGuidanceMixin,
    AddAudioGuidanceMixin, TaskSerializer

):
    """Расширеный сериализатор заданий."""

    images = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    def get_images(self, instance):
        """Получить изображения для задания."""
        queryset = Image.objects.filter(
            parent_tasks__task=instance
        ).order_by('parent_tasks__number')

        return ImageSerializer(queryset, many=True).data

    def get_questions(self, instance):
        """Получить вопросы для задания."""
        queryset = Question.objects.filter(
            parent_tasks__task=instance
        ).order_by('parent_tasks__number')

        return self.add_question_guidance(
            QuestionSerializer(queryset, many=True).data
        )

    def to_representation(self, instance):
        """Преобразование в объект."""
        obj = self.add_task_guidance(
            instance.type, super().to_representation(instance)
        )

        if instance.type == TaskType.INTERVIEW:
            return self.add_guidance(obj, only_types=[
                AudioGuidanceType.INTERVIEW_END,
            ])

        return self.add_guidance(obj, only_types=[
            AudioGuidanceType.BEFORE_TASK_EXECUTION,
        ])

    class Meta:
        model = Task
        fields = [
            'id',
            'type',
            'header',
            'description',
            'images',
            'questions',
        ]


class ExamSerializer(serializers.ModelSerializer):
    """Сериализатор модели экзамены."""

    type = EnumField(
        enum_class=ExamType
    )

    class Meta:
        model = Exam
        fields = [
            'id',
            'number',
            'type'
        ]


class ExtendedExamSerializer(AddAudioGuidanceMixin, ExamSerializer):
    """Расширеный сериализатор модели экзамены."""

    tasks = serializers.SerializerMethodField()

    def get_tasks(self, instance):
        """Получить задания для экзамена."""
        tasks = Task.objects.filter(
            exams__exam=instance
        ).annotate(
            task_number=Subquery(
                TaskTypeParameter.objects.filter(
                    type=OuterRef('type')
                ).values('number')[:1]
            )
        ).order_by('task_number')

        return ExtendedTaskSerializer(tasks, many=True).data

    def to_representation(self, instance):
        """Преобразование в объект."""
        obj = super().to_representation(instance)
        return self.add_guidance(obj, only_types=[
            AudioGuidanceType.START_EXAM,
            AudioGuidanceType.END_EXAM
        ])

    class Meta:
        model = Exam
        fields = [
            'id',
            'number',
            'type',
            'tasks'
        ]


class QuestionAnswerSerializer(serializers.Serializer):
    """Сериализатор для вопросов в ответах."""

    question_id = serializers.IntegerField()
    audio = Base64FileField()


class TaskAnswerSerializer(serializers.Serializer):
    """Сериализатор для вопросов в ответах."""

    task_id = serializers.IntegerField()
    audio = Base64FileField(allow_null=True, required=False)
    questions = QuestionAnswerSerializer(many=True, required=False)


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответов."""

    def to_representation(self, instance):
        """Преобразование в объект."""
        representation = super().to_representation(instance)
        if representation['answer_archive']:
            representation['answer_archive'] = os.path.join(
                settings.MEDIA_URL, instance.answer_archive.name
            )
        return representation

    class Meta:
        model = Answer
        fields = [
            'id',
            'created_at',
            'answer_archive',
        ]
