from django.contrib import admin

from trainer_backend.core.db.mixins import ModelAdminDisplayNameMixin
from trainer_backend.trainer.admin.relative import ImagesInTaskInline
from trainer_backend.trainer.admin.relative import QuestionsInTaskInline
from trainer_backend.trainer.admin.relative import TasksInExamInline
from trainer_backend.trainer.forms import ExamForm
from trainer_backend.trainer.forms import ImageForm
from trainer_backend.trainer.forms import QuestionForm
from trainer_backend.trainer.forms import TaskForm
from trainer_backend.trainer.forms import ThematicSpeechContentForm
from trainer_backend.trainer.models import Exam
from trainer_backend.trainer.models import Image
from trainer_backend.trainer.models import Question
from trainer_backend.trainer.models import Task
from trainer_backend.trainer.models import ThematicSpeechContent


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Админ панель для работы с изображениями."""

    form = ImageForm
    list_display = (
        'header', 'image'
    )


@admin.register(Question)
class QuestionAdmin(ModelAdminDisplayNameMixin, admin.ModelAdmin):
    """Админ панель для работы с вопросами."""

    form = QuestionForm
    list_display = ('display_name', 'description',)


@admin.register(ThematicSpeechContent)
class ThematicSpeechContentAdmin(admin.ModelAdmin):
    """Админ панель для работы с тематическим содержанием речи."""

    form = ThematicSpeechContentForm
    list_display = (
        'short_designation', 'description'
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Админ панель для заданий."""

    form = TaskForm
    list_display = ('header', 'description', 'thematic_speech_content')

    inlines = [
        ImagesInTaskInline,
        QuestionsInTaskInline,
    ]


@admin.register(Exam)
class ExamAdmin(ModelAdminDisplayNameMixin, admin.ModelAdmin):
    """Админ панель для экзаменов."""

    form = ExamForm
    list_display = ('display_name', 'fipi', 'exam_type')
    inlines = [TasksInExamInline]
