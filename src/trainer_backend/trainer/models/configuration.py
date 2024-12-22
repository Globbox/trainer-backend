from django.db import models
from django.dispatch import receiver

from trainer_backend.trainer.enums import AudioGuidanceType
from trainer_backend.trainer.enums import TaskType

from .base import ModelWithAudioFileMixin


class AudioGuidance(ModelWithAudioFileMixin, models.Model):
    """Модель для хранения аудио сопровождения."""

    guidance_type = models.PositiveSmallIntegerField(
        unique=True,
        choices=AudioGuidanceType.choices(),
        verbose_name="Тип аудио сопровождения",
    )

    audio = models.FileField(
        upload_to='guidance/',
        verbose_name='Аудио файл',
    )

    def __str__(self):
        return AudioGuidanceType.get(self.guidance_type).display

    class Meta:
        verbose_name = "Аудио сопровождение"
        verbose_name_plural = "Аудио сопровождения"


class QuestionAudioGuidance(
    ModelWithAudioFileMixin, models.Model
):
    """Модель для хранения аудио сопровождения вопросов."""

    question_number = models.PositiveIntegerField(
        unique=True,
        verbose_name="Номер вопроса",
    )

    audio = models.FileField(
        upload_to='guidance/',
        verbose_name='Аудио файл',
    )
    def __str__(self):
        return f'Аудио сопровождения вопроса {self.question_number}'

    class Meta:
        verbose_name = "Аудио сопровождение вопросов"
        verbose_name_plural = "Аудио сопровождения вопросов"


class TaskTypeParameter(ModelWithAudioFileMixin, models.Model):
    """Параметры для типов заданий."""

    task_type = models.SmallIntegerField(
        unique=True,
        choices=TaskType.choices(),
        verbose_name='Тип задания',
    )
    number = models.PositiveIntegerField(
        verbose_name="Порядок задания в экзамене"
    )
    audio = models.FileField(
        upload_to='guidance/',
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

    class Meta:
        unique_together = (('task_type', 'number'),)
        verbose_name = "Параметр для типов заданий"
        verbose_name_plural = "Параметры для типов заданий"


@receiver(models.signals.post_delete, sender=AudioGuidance)
@receiver(models.signals.post_delete, sender=TaskTypeParameter)
@receiver(models.signals.post_delete, sender=QuestionAudioGuidance)
def auto_delete_audio_file(sender, instance, **kwargs):
    """Удаление файла при удалении записи."""
    if instance.audio:
        instance.audio.delete(save=False)
