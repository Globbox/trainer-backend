from django import forms

from trainer_backend.trainer.models import ImagesInTask
from trainer_backend.trainer.models import QuestionsInTask
from trainer_backend.trainer.models import TasksInExam


class TasksInExamForm(forms.ModelForm):
    """Форма для редактирования заданий в экзаменах."""

    class Meta:
        model = TasksInExam
        fields = '__all__'


class ImagesInTaskForm(forms.ModelForm):
    """Форма для редактирования изображений в заданиях."""

    number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '1'}),
        label='Номер изображения в задании'
    )

    class Meta:
        model = ImagesInTask
        fields = '__all__'


class QuestionsInTaskForm(forms.ModelForm):
    """Форма для редактирования вопросов в заданиях."""

    number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '1'}),
        label='Номер вопроса в задании'
    )

    class Meta:
        model = QuestionsInTask
        fields = '__all__'
