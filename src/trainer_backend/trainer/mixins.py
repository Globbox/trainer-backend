from typing import Sequence
from typing import Type
from typing import Union
from urllib.parse import urljoin

from django.conf import settings

from trainer_backend.core.file.mixins import FilePathMixin

from .enums import AudioGuidanceType
from .mappers import AUDIO_GUIDANCE_FIELD_MAPPER
from .models import AudioGuidance
from .models import QuestionAudioGuidance
from .models import TaskTypeParameter


class AddAudioGuidanceMixin(FilePathMixin):
    """Миксин расширяющий класс для добавления аудио сопровождения."""

    _only_types: Union[Sequence[Type[AudioGuidanceType]], None]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        audio_guidance = AudioGuidance.objects.all()
        if self._only_types is not None and len(self._only_types) > 0:
            audio_guidance = audio_guidance.filter(
                guidance_type__in=self._only_types
            )

        self._audio_guidance_map = dict(
            audio_guidance.values_list('guidance_type', 'audio')
        )

    def add_guidance(self, instance):
        """Добавить аудио сопровождение."""
        for guidance_type, guidance_url in self._audio_guidance_map.items():
            field = AUDIO_GUIDANCE_FIELD_MAPPER.get(guidance_type)
            if field is None:
                continue
            instance[field] = self._get_file_path(guidance_url)

        return instance


class TaskParametersMixin:
    """Миксин расширяющий класс задач."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._task_params_map = {
            task.task_type: {
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
    #
    # def _get_task_params(self, task_type):
    #     """Получить параметры задания."""
    #     return TaskParameterSerializer(self._task_params_map.get(
    #         task_type
    #     )).data


class AddQuestionAudioGuidanceMixin:
    """Миксин для добавления аудио сопровождения вопросов."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._questions_guidance = QuestionAudioGuidance.objects.order_by(
            'question_number'
        )

    def add_question_guidance(self, questions):
        """Добавить аудио сопровождение."""
        questions_guidance = self._questions_guidance
        if len(questions) > len(questions_guidance):
            questions_guidance += [{
                'audio_guidance': None
            }] * (len(questions) - len(questions_guidance))
        return list(
            {
                'audio_guidance': urljoin(
                    settings.MEDIA_URL, guidance.audio.url
                ),
                **task
            }
            for task, guidance in zip(questions, questions_guidance)
        )
