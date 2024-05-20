from django.conf import settings
from django.db import models

from trainer_backend.core.file.utils import upload_hash_file

from .base import Question
from .base import Task


class Answer(models.Model):
    """Модель ответов пользователей."""

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    user = models.ForeignKey(
        'user.User',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='answers'
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
        upload_to=upload_hash_file(
            'audio_answer',
            settings.AUDIO_TASK_DIR,
        ),
        verbose_name='Аудио задание',
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
        upload_to=upload_hash_file(
            'audio_answer',
            settings.AUDIO_TASK_DIR,
        ),
        verbose_name='Аудио задание',
    )

    class Meta:
        unique_together = ('task', 'question')
        verbose_name = "Ответ пользователя к вопросу"
        verbose_name_plural = "Ответы пользователя к вопросам"
