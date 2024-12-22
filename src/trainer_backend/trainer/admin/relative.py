from django.contrib import admin

from trainer_backend.trainer.forms import ImagesInTaskForm
from trainer_backend.trainer.forms import QuestionsInTaskForm
from trainer_backend.trainer.forms import TasksInExamForm
from trainer_backend.trainer.models import ImagesInTask
from trainer_backend.trainer.models import QuestionsInTask
from trainer_backend.trainer.models import TasksInExam


class QuestionsInTaskInline(admin.TabularInline):
    """Админ панель для вопросов в заданиях."""

    form = QuestionsInTaskForm
    model = QuestionsInTask
    extra = 0
    min_num = 0
    verbose_name = "Вопрос"
    verbose_name_plural = "Вопросы"


class ImagesInTaskInline(admin.TabularInline):
    """Админ панель для изображений в заданиях."""

    form = ImagesInTaskForm
    model = ImagesInTask
    extra = 0
    min_num = 0
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"


class TasksInExamInline(admin.TabularInline):
    """Админ панель для изображений в заданиях."""

    model = TasksInExam
    form = TasksInExamForm
    extra = 0
    min_num = 1
    verbose_name = "Задание"
    verbose_name_plural = "Задания"
