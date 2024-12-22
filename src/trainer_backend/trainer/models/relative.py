from django.db import models

from .base import Exam
from .base import Image
from .base import Question
from .base import Task


class ImagesInTask(models.Model):
    """Модель связи изображений в задании."""

    number = models.PositiveIntegerField(
        verbose_name="Порядок изображений в задании"
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name="Основное задание",
        related_name='images'
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        verbose_name="Изображения",
        related_name='parent_tasks'
    )

    class Meta:
        unique_together = ('task', 'number')
        verbose_name = "Изображения в задании"
        verbose_name_plural = "Изображений в задании"


class QuestionsInTask(models.Model):
    """Модель связи вопросов в задании."""

    number = models.PositiveIntegerField(
        verbose_name="Порядок вопросов в задании"
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name="Основное задание",
        related_name='questions'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Вопросы",
        related_name='parent_tasks'
    )

    class Meta:
        unique_together = ('task', 'question', 'number')
        verbose_name = "Вопрос в задании"
        verbose_name_plural = "Вопросы в задании"


class TasksInExam(models.Model):
    """Модель связи Заданий и Экзаменов."""

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        verbose_name="Экзамен",
        related_name='tasks'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name="Задание",
        related_name='exams'
    )

    class Meta:
        unique_together = ('exam', 'task')
        verbose_name = "Задание в экзамене"
        verbose_name_plural = "Задания в экзамене"
