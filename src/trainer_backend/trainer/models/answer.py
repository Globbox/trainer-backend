from django.db import models
from django.dispatch import receiver

from ..enums import AnswerStatus
from .base import Question
from .base import Task


class Answer(models.Model):
    """Модель ответов пользователей."""

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    status = models.SmallIntegerField(
        default=AnswerStatus.UNPROCESSED.value,
        choices=AnswerStatus.choices(),
    )
    user = models.ForeignKey(
        'user.User',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='answers'
    )
    full_audio = models.FileField(
        null=True,
        blank=True,
        upload_to='answer/',
        verbose_name='Полный ответ пользователя',
    )
    answer_archive = models.FileField(
        null=True,
        blank=True,
        upload_to='answer/',
        verbose_name='Архив ответа',
    )

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"


class TaskAnswer(models.Model):
    """Модель ответов к заданиям."""

    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name="Ответ пользователя",
        related_name='tasks'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name="Задание",
        related_name='answers'
    )
    task_number = models.PositiveIntegerField(
        null=True,
        verbose_name="Номер задания"
    )
    audio = models.FileField(
        null=True,
        blank=True,
        upload_to='answer/',
        verbose_name='Ответ на задание',
    )

    class Meta:
        unique_together = ('answer', 'task')
        verbose_name = "Ответ пользователя к заданию"
        verbose_name_plural = "Ответы пользователя к заданиям"


class QuestionAnswer(models.Model):
    """Модель ответов к вопросам."""

    task = models.ForeignKey(
        TaskAnswer,
        on_delete=models.CASCADE,
        verbose_name="Ответ к заданию",
        related_name='questions'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Вопрос",
        related_name='answers'
    )
    question_number = models.PositiveIntegerField(
        null=True,
        verbose_name="Номер вопроса"
    )
    audio = models.FileField(
        upload_to='answer/',
        verbose_name='Ответ на вопрос',
    )

    class Meta:
        unique_together = ('task', 'question')
        verbose_name = "Ответ пользователя к вопросу"
        verbose_name_plural = "Ответы пользователя к вопросам"


@receiver(models.signals.post_delete, sender=QuestionAnswer)
@receiver(models.signals.post_delete, sender=TaskAnswer)
def auto_delete_audio_files(sender, instance, **kwargs):
    """Удаление файла при удалении записи."""
    if instance.audio:
        instance.audio.delete(save=False)


@receiver(models.signals.post_delete, sender=Answer)
def auto_delete_answer_files(sender, instance, **kwargs):
    """Удаление файлов при удалении записи."""
    if instance.full_audio:
        instance.full_audio.delete(save=False)
    if instance.answer_archive:
        instance.answer_archive.delete(save=False)
