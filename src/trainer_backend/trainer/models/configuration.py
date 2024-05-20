from django.conf import settings
from django.db import models

from trainer_backend.core.file.mixins import AudioFileConvertMixin
from trainer_backend.core.file.utils import upload_hash_file
from trainer_backend.trainer.enums import AudioGuidanceType
from trainer_backend.trainer.enums import TaskType


class AudioGuidance(AudioFileConvertMixin, models.Model):
    """Модель для хранения аудио сопровождения."""

    guidance_type = models.PositiveSmallIntegerField(
        unique=True,
        choices=AudioGuidanceType.choices(),
        verbose_name="Тип аудио сопровождения",
    )

    audio = models.FileField(
        upload_to=upload_hash_file(
            'audio',
            settings.AUDIO_GUIDANCE_DIR,
        ),
        verbose_name='Аудио файл',
    )

    def __str__(self):
        return AudioGuidanceType.get(self.guidance_type).display

    def clean(self):
        """Обработка перед изменением/добавлением."""
        super(AudioGuidance, self).clean()
        self.audio = self.convert_audio(self.audio)

    class Meta:
        verbose_name = "Аудио сопровождение"
        verbose_name_plural = "Аудио сопровождения"


class QuestionAudioGuidance(models.Model, AudioFileConvertMixin):
    """Модель для хранения аудио сопровождения вопросов."""

    question_number = models.PositiveIntegerField(
        unique=True,
        verbose_name="Номер вопроса",
    )

    audio = models.FileField(
        upload_to=upload_hash_file(
            'audio',
            settings.AUDIO_GUIDANCE_DIR,
        ),
        verbose_name='Аудио файл',
    )

    def __str__(self):
        return f'Аудио сопровождения вопроса {self.question_number}'

    def clean(self):
        """Обработка перед изменением/добавлением."""
        super(QuestionAudioGuidance, self).clean()
        self.audio = self.convert_audio(self.audio)

    class Meta:
        verbose_name = "Аудио сопровождение вопросов"
        verbose_name_plural = "Аудио сопровождения вопросов"


class TaskTypeParameter(models.Model, AudioFileConvertMixin):
    """Параметры для типов заданий."""

    type = models.SmallIntegerField(
        unique=True,
        choices=TaskType.choices(),
        verbose_name='Тип задания',
    )
    number = models.PositiveIntegerField(
        verbose_name="Порядок задания в экзамене"
    )
    audio = models.FileField(
        upload_to=upload_hash_file(
            'audio',
            settings.AUDIO_GUIDANCE_DIR,
        ),
        verbose_name='Аудио сопровождение',
    )
    preparation_seconds = models.PositiveIntegerField(
        verbose_name='Кол-во секунд на подготовку задания',
    )
    execution_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Кол-во секунд на выполнение задания',
    )
    question_execution_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Кол-во секунд на ответ',
    )

    def clean(self):
        """Обработка перед изменением/добавлением."""
        super(TaskTypeParameter, self).clean()
        self.audio = self.convert_audio(self.audio)

    class Meta:
        unique_together = (('type', 'number'),)
        verbose_name = "Параметр для типов заданий"
        verbose_name_plural = "Параметры для типов заданий"
