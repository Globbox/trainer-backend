from urllib.parse import urljoin

from django.conf import settings

from .mappers import AudioGuidanceFieldMapper
from .models import AudioGuidance
from .models import QuestionAudioGuidance
from .models import TaskTypeParameter


class AddAudioGuidanceMixin:
    """Миксин расширяющий класс для добавления аудио сопровождения задач."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._audio_guidance_map = dict(
            AudioGuidance.objects.values_list('guidance_type', 'audio')
        )

    def add_guidance(self, obj, only_types=None):
        """Добавить аудио сопровождение."""
        return {**obj, **{
            v: urljoin(settings.MEDIA_URL, self._audio_guidance_map.get(k))
            for k, v in AudioGuidanceFieldMapper.items()
            if only_types is None or k in only_types
        }}


class AddTaskParametersMixin:
    """Миксин расширяющий класс задач."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._audio_task_guidance_map = {
            task.type: {
                'number': task.number,
                'audio_guidance': task.audio.url,
                'preparation_seconds': task.preparation_seconds,
                'execution_seconds': task.execution_seconds,
                'question_execution_seconds': (
                    task.question_execution_seconds
                ),
            }
            for task in TaskTypeParameter.objects.all()
        }

    def add_task_guidance(self, task_type, instance):
        """Добавить аудио сопровождение."""
        audio_guidance = self._audio_task_guidance_map.get(task_type)
        if audio_guidance is None:
            return instance

        return {**instance, **audio_guidance}

    def add_task_number(self, task_type, instance):
        """Добавить номер задания."""
        task_mixin = self._audio_task_guidance_map.get(task_type)

        if task_mixin is not None:
            instance['number'] = task_mixin['number']

        return instance


class AddQuestionAudioGuidanceMixin:
    """Миксин расширяющий класс для добавления аудио сопровождения вопросов."""

    def add_question_guidance(self, questions):
        """Добавить аудио сопровождение."""
        questions_guidance = QuestionAudioGuidance.objects.all().order_by(
            'question_number'
        ).values(
            'audio'
        )

        return list(
            {
                'audio_guidance': urljoin(
                    settings.MEDIA_URL, guidance['audio']
                ),
                **task
            }
            for task, guidance in zip(questions, questions_guidance)
        )
