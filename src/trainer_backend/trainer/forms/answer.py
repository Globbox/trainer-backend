from django import forms

from trainer_backend.core.file.mixins import AudioFileFieldAdminMixin
from trainer_backend.trainer.models import Answer
from trainer_backend.trainer.models import QuestionAnswer
from trainer_backend.trainer.models import TaskAnswer


class AnswerForm(forms.ModelForm):
    """Форма редактирования ответа."""

    class Meta:
        model = Answer
        fields = ['user']


class QuestionAnswerForm(forms.ModelForm, AudioFileFieldAdminMixin):
    """Форма редактирования вопроса в задании."""

    class Meta:
        model = QuestionAnswer
        fields = ['question', 'question_number', 'audio']
        widgets = {
            'audio': forms.ClearableFileInput(
                attrs={'accept': 'audio/*', }
            ),
        }


class TaskAnswerForm(forms.ModelForm, AudioFileFieldAdminMixin):
    """Форма редактирования задания в ответе."""

    class Meta:
        model = TaskAnswer
        fields = ['task', 'task_number', 'audio']
        widgets = {
            'audio': forms.ClearableFileInput(
                attrs={'accept': 'audio/*', }
            ),
        }
