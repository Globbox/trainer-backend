from django.contrib import admin

from trainer_backend.core.file.mixins import AudioFileFieldAdminMixin
from trainer_backend.trainer.forms import AudioGuidanceForm
from trainer_backend.trainer.forms import QuestionAudioGuidanceForm
from trainer_backend.trainer.forms import TaskTypeParameterForm
from trainer_backend.trainer.models import AudioGuidance
from trainer_backend.trainer.models import QuestionAudioGuidance
from trainer_backend.trainer.models import TaskTypeParameter


@admin.register(AudioGuidance)
class AudioGuidanceAdmin(admin.ModelAdmin, AudioFileFieldAdminMixin):
    """Класс для администрирования аудио сопровождения."""

    form = AudioGuidanceForm
    list_display = ('guidance_type', 'audio_preview')
    readonly_fields = ('audio_preview',)


@admin.register(QuestionAudioGuidance)
class TaskAudioGuidanceAdmin(admin.ModelAdmin, AudioFileFieldAdminMixin):
    """Класс для администрирования аудио сопровождения вопросов."""

    form = QuestionAudioGuidanceForm
    list_display = ('question_number', 'audio_preview')
    readonly_fields = ('audio_preview',)


@admin.register(TaskTypeParameter)
class TaskTypeParameterAdmin(admin.ModelAdmin, AudioFileFieldAdminMixin):
    """Класс для администрирования параметров для заданий."""

    form = TaskTypeParameterForm
    list_display = ('type', 'audio_preview')
    readonly_fields = ('audio_preview',)
