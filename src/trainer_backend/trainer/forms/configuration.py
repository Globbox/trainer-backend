from django import forms

from trainer_backend.trainer.models import AudioGuidance
from trainer_backend.trainer.models import QuestionAudioGuidance
from trainer_backend.trainer.models import TaskTypeParameter


class AudioGuidanceForm(forms.ModelForm):
    """Форма аудио сопровождения."""

    class Meta:
        model = AudioGuidance
        fields = ['guidance_type', 'audio']
        widgets = {
            'audio': forms.ClearableFileInput(
                attrs={'accept': 'audio/*', }
            ),
        }


class QuestionAudioGuidanceForm(forms.ModelForm):
    """Форма аудио сопровождения вопросов."""

    question_number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '1'}),
        label='Номер вопроса в задании'
    )

    class Meta:
        model = QuestionAudioGuidance
        fields = ['question_number', 'audio']
        widgets = {
            'audio': forms.ClearableFileInput(
                attrs={'accept': 'audio/*', }
            ),
        }


class TaskTypeParameterForm(forms.ModelForm):
    """Форма параметров для заданий."""

    number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '1'}),
        label="Порядок задания в экзамене"
    )

    class Meta:
        model = TaskTypeParameter
        fields = ['exam_type', 'task_type', 'number', 'audio',
                  'preparation_seconds', 'execution_seconds',
                  'question_execution_seconds']
        widgets = {
            'audio': forms.ClearableFileInput(
                attrs={'accept': 'audio/*', }
            ),
        }
