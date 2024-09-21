from django import forms

from trainer_backend.core.file.mixins import AudioFileFieldAdminMixin
from trainer_backend.core.widgets.markdown import MarkdownWidget
from trainer_backend.trainer.models import Exam
from trainer_backend.trainer.models import Image
from trainer_backend.trainer.models import Question
from trainer_backend.trainer.models import Task
from trainer_backend.trainer.models import ThematicSpeechContent


class ImageForm(forms.ModelForm):
    """Форма для изображений."""

    class Meta:
        model = Image
        fields = ['header', 'image']
        widgets = {
            'image': forms.ClearableFileInput(
                attrs={'accept': 'image/*', }
            ),
        }


class ExamForm(forms.ModelForm):
    """Форма для редактирования экзаменов."""

    number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '1'}),
        label='Номер экзамена'
    )

    class Meta:
        model = Exam
        fields = '__all__'


class ThematicSpeechContentForm(forms.ModelForm):
    """Форма тематического содержания речи."""

    class Meta:
        model = ThematicSpeechContent
        fields = '__all__'


class TaskForm(forms.ModelForm, AudioFileFieldAdminMixin):
    """Форма для редактирования модели Задание."""

    header = forms.CharField(
        widget=MarkdownWidget,
        label='Заголовок'
    )
    description = forms.CharField(
        widget=MarkdownWidget,
        required=False,
        label='Описание'
    )

    class Meta:
        model = Task
        fields = [
            'task_type',
            'header',
            'description',
            'audio',
            'thematic_speech_content',
        ]
        widgets = {
            'audio': forms.ClearableFileInput(
                attrs={'accept': 'audio/*', }
            ),
        }


class QuestionForm(forms.ModelForm):
    """Форма для редактирования вопроса."""

    class Meta:
        model = Question
        fields = [
            'description',
            'audio',
        ]
