from django.contrib import admin

from trainer_backend.trainer.forms import AnswerForm
from trainer_backend.trainer.forms import QuestionAnswerForm
from trainer_backend.trainer.forms import TaskAnswerForm
from trainer_backend.trainer.models import Answer
from trainer_backend.trainer.models import QuestionAnswer
from trainer_backend.trainer.models import TaskAnswer


class QuestionAnswerInline(admin.TabularInline):
    """Админ панель вопросов в задании."""

    form = QuestionAnswerForm
    model = QuestionAnswer
    extra = 0
    min_num = 0
    verbose_name = "Вопросы"
    verbose_name_plural = "Вопросы"


class TaskAnswerInline(admin.TabularInline):
    """Админ панель заданий в ответе."""

    form = TaskAnswerForm
    model = TaskAnswer
    inlines = [QuestionAnswerInline]
    extra = 0
    min_num = 0
    verbose_name = "Задания"
    verbose_name_plural = "Задания"


@admin.register(TaskAnswer)
class TaskAnswerAdmin(admin.ModelAdmin):
    """Админ панель заданий в ответе."""

    form = TaskAnswerForm
    list_display = ('task', 'task_number', 'audio')

    inlines = [QuestionAnswerInline]


@admin.register(Answer)
class TaskAdmin(admin.ModelAdmin):
    """Админ панель для заданий."""

    form = AnswerForm
    list_display = ('user', 'created_at',)

    inlines = [TaskAnswerInline]
